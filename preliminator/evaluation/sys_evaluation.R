# Placeholder script for system evaluation

# Load necessary packages
library(RJSONIO)
library(RCurl)
library(MASS)
library(leaps)
library(ggplot2)

# Import data from json files
for(file in c('candidate.json', 'transcript.json', 'presurvey.json', 'postsurvey.json')) {
  # Strip file tag
  file.name <- gsub(".json", "", file)
  
  # Catch empty 'feedback.json' file exception
  if(file.name == 'feedback') next
  
  # Read in data from json file
  assign(file.name, fromJSON(paste(readLines(file, warn = FALSE), collapse = "")))
  
  # Save field names
  field.names <- names(eval(parse(text = file.name))[[1]]$fields)
  
  # Get number of columns
  num.col <- length(eval(parse(text = file.name))[[1]]$fields)
  
  # Coerce to dataframe
  assign(file.name, data.frame(matrix(unlist(sapply(eval(parse(text = file.name)), "[[", 3)), ncol = num.col, byrow = TRUE), stringsAsFactors = FALSE))

  # Re-establish field names and set all variables as characters
  temp <- eval(parse(text = file.name))
  colnames(temp) <- field.names
  assign(file.name, temp)
}

# Manually fix interview number bug (always '1')
curr_interview <- 1
for(row in 2:nrow(transcript)) {

  if (any(grepl("Hello", transcript[row, "line_contents"])) == TRUE) {
    curr_interview <- curr_interview + 1
  }
  
  transcript[row, "interview"] <- curr_interview
  
}

# Manually identify subset of usable data (starting at row 227)
candidate <- candidate[227:nrow(candidate),]

# Identify length of usable chunk
tail.len <- nrow(candidate)

# Extract relevant subset of transcript (last 21 sets of each)
transcript$interview <- as.numeric(transcript$interview)
transcript.limit <- as.numeric(tail(transcript$interview,1)) - tail.len
transcript <- transcript[which((transcript$interview >= transcript.limit) & (transcript$interview < tail(transcript$interview, 1))),]

# Extract relevant susbset of pre-/post-surveys
presurvey <- presurvey[(nrow(presurvey) - tail.len + 1):nrow(presurvey),]
postsurvey <- postsurvey[(nrow(postsurvey) - tail.len + 1):nrow(postsurvey),]

# Candidate field name
colnames(candidate)[1] <- "interview"

# Survey field names
names(presurvey) <- c("interview", "pre.interest.level", "pre.satisfaction", "pre.asr.confidence", "pre.ease.of.use", "pre.previous.experience")
names(postsurvey) <- c("interview", "post.interest.level", "post.satisfaction", "post.asr.confidence", "post.ease.of.use", "post.previous.experience")

# Long form survey names
presurvey.names.long <- c("I am interested in using dialogue systems to help me with tasks.",
                          "I believe this system will help prepare me for interviews.",
                          "I am confident this system will understand me majority of the time.",
                          "I believe this system will be easy to use.",
                          "I have previous experience using dialogue systems.")

postsurvey.names.long <- c("This system has sustained or fostered my interest in using dialogue systems to help me with tasks.",
                           "If I had the chance, I would use this system again in order to prepare for interviews.",
                           "I am confident this system understood me majority of the time.",
                           "This system was easy to use.",
                           "I believe my previous experience helped me use this dialogue system.")


# Build feature set from transcript
transcript.set <- data.frame(interview = numeric(0), 
                             total.utterances = numeric(0), 
                             system.words = numeric(0), 
                             user.words = numeric(0),
                             avg.system.utterance.len = numeric(0),
                             avg.user.utterance.len = numeric(0),
                             avg.system.word.len = numeric(0),
                             avg.user.word.len = numeric(0),
                             quite.count = numeric(0),
                             back.count = numeric(0))
interview.number <- 1

for(interview in unique(transcript$interview)) {
  # Get interview data subset
  subset <- transcript[which(transcript$interview == interview),]
  
  # Get features of interest
  feature.set <- interview.number
  
  # Count total utterances
  feature.set <- c(feature.set, nrow(subset))
  
  # Count system words
  feature.set <- c(feature.set, length(strsplit(paste(subset[which(subset$speaker == "R"), "line_contents"], collapse = " "), split = " ")[[1]]))
  
  # Count user words
  feature.set <- c(feature.set, length(strsplit(paste(subset[which(subset$speaker == "C"), "line_contents"], collapse = " "), split = " ")[[1]]))
  
  # Average system utterance length
  feature.set <- c(feature.set, mean(unlist(lapply(subset[which(subset$speaker == "R"), "line_contents"], FUN = function(x) length(strsplit(x, split = " ")[[1]])))))
  
  # Average candidate utterance length
  feature.set <- c(feature.set, mean(unlist(lapply(subset[which(subset$speaker == "C"), "line_contents"], FUN = function(x) length(strsplit(x, split = " ")[[1]])))))
  
  # Average system word length
  feature.set <- c(feature.set, mean(unlist(lapply(strsplit(paste(subset[which(subset$speaker == "R"), "line_contents"], collapse = " "), split = " ")[[1]], nchar))))
  
  # Average user word length
  feature.set <- c(feature.set, mean(unlist(lapply(strsplit(paste(subset[which(subset$speaker == "C"), "line_contents"], collapse = " "), split = " ")[[1]], nchar))))
  
  # Quite count
  feature.set <- c(feature.set, sum(unlist(lapply(subset[which(subset$speaker == "C"), "line_contents"], FUN = function(x) grepl("quite", x)))))
  
  # Back count
  feature.set <- c(feature.set, sum(unlist(lapply(subset[which(subset$speaker == "C"), "line_contents"], FUN = function(x) grepl("back", x)))))
  
  # Append feature set to transcript.set row
  transcript.set[interview.number,] <- feature.set
  
  # Iterate for next interview
  interview.number <- interview.number + 1
}

# Renumber data sets
candidate$interview <- 1:nrow(candidate)
presurvey$interview <- 1:nrow(presurvey)
postsurvey$interview <- 1:nrow(postsurvey)

# Cast as numeric
presurvey <- sapply(presurvey, as.numeric)
postsurvey <- sapply(postsurvey, as.numeric)

# Bind together data sets
dialg.sys.data <- merge(candidate, transcript.set, by = "interview")
dialg.sys.data <- merge(dialg.sys.data, presurvey, by = "interview")
dialg.sys.data <- merge(dialg.sys.data, postsurvey, by = "interview")

# Get survey diffs
dialg.sys.data$interest.level <- dialg.sys.data$post.interest.level - dialg.sys.data$pre.interest.level
dialg.sys.data$satisfaction <- dialg.sys.data$post.satisfaction - dialg.sys.data$pre.satisfaction
dialg.sys.data$asr.confidence <- dialg.sys.data$post.asr.confidence - dialg.sys.data$pre.asr.confidence
dialg.sys.data$ease.of.use <- dialg.sys.data$post.ease.of.use - dialg.sys.data$pre.ease.of.use
dialg.sys.data$previous.experience <- dialg.sys.data$post.previous.experience - dialg.sys.data$pre.previous.experience

# Write data table for sharing purposes
write.csv(dialg.sys.data, file = "dialg.sys.data.csv", row.names = FALSE)

# Insufficient data for reasonable cross validation

## Find best predictor of user satisfaction

# Apply Stepwise Regression
fit.stepwise <- lm(satisfaction ~ avg.system.utterance.len + 
                     avg.user.utterance.len +
                     avg.system.word.len +
                     avg.user.word.len +
                     interest.level + 
                     asr.confidence + 
                     ease.of.use + 
                     previous.experience, data = dialg.sys.data)
step <- stepAIC(fit.stepwise, directions = "both")
step

# Apply all-subsets regression
fit.leaps <- regsubsets(satisfaction ~ avg.system.utterance.len + 
                            avg.user.utterance.len +
                            avg.system.word.len +
                            avg.user.word.len +
                            interest.level + 
                            asr.confidence + 
                            ease.of.use + 
                            previous.experience, data = dialg.sys.data, nbest = 3, nvmax = 4)
#summary(fit.leaps)

# Modify plot.regsubsets function
plot.regsubsets<-function(x,labels=obj$xnames,main=NULL,
                          scale=c("bic","Cp","adjr2","r2"),
                          col=gray(seq(0,0.9,length=10)),mar = c(7,5,6,3)+0.1, ...){
  obj<-x
  lsum<-summary(obj)
  par(mar=mar)
  nmodels<-length(lsum$rsq)
  np<-obj$np
  propscale<-FALSE
  sscale<-pmatch(scale[1],c("bic","Cp","adjr2","r2"),nomatch=0)
  if (sscale==0)
    stop(paste("Unrecognised scale=",scale))
  if (propscale)
    stop(paste("Proportional scaling only for probabilities"))
  
  yscale<-switch(sscale,lsum$bic,lsum$cp,lsum$adjr2,lsum$rsq)
  up<-switch(sscale,-1,-1,1,1)
  
  index<-order(yscale*up)
  
  colorscale<- switch(sscale,
                      yscale,yscale,
                      -log(pmax(yscale,0.0001)),-log(pmax(yscale,0.0001)))
  
  image(z=t(ifelse(lsum$which[index,],
                   colorscale[index],NA+max(colorscale)*1.5)),
        xaxt="n",yaxt="n",x=(1:np),y=1:nmodels,xlab="",ylab=scale[1],col=col)
  
  laspar<-par("las")
  on.exit(par(las=laspar))
  par(las=2)
  axis(1,at=1:np,labels=labels)
  axis(2,at=1:nmodels,labels=signif(yscale[index],2))
  
  if (!is.null(main))
    title(main=main)
  box()
  invisible(NULL)
}

plot(fit.leaps, scale = "r2", mar = c(15,4.1,4.1,2.1), main = "Regression Model Selection (for Satisfaction)", labels = c("Intercept", "Average System Utterance Length",
                                                                              "Average User Utterance Length",
                                                                              "Averge System Word Length",
                                                                              "Average User Word Length",
                                                                              "Interest Level",
                                                                              "ASR Confidence",
                                                                              "Ease of Use",
                                                                              "Previous Experience"))

library(car)

## Adjusted R2
## Plot some distributions

# Density plots for average utterance length
dist.data <- data.frame(source = "system", avg.utterance.len =  dialg.sys.data$avg.system.utterance.len)
dist.data <- rbind(dist.data, data.frame(source = "user", avg.utterance.len =  dialg.sys.data$avg.user.utterance.len))
ggplot(dist.data, aes(x = avg.utterance.len, fill = source)) + geom_density(alpha=.3)  +
  xlab("Average Utterance Length (words)") +
  ylab("Density") +
  ggtitle("Density Plot of Average Utterance Length")  + theme(legend.text=element_text(size=12))


# Density plot for total words spoken
dist.data <- data.frame(source = "system", avg.word.len =  dialg.sys.data$avg.system.word.len)
dist.data <- rbind(dist.data, data.frame(source = "user", avg.word.len =  dialg.sys.data$avg.user.word.len))
ggplot(dist.data, aes(x = avg.word.len, fill = source)) + geom_density(alpha=.3)  +
  xlab("Average Word Length (characters)") +
  ylab("Density") +
  ggtitle("Density Plot of Average Word Length")  + theme(legend.text=element_text(size=12))


# Density plots of survey outcomes
survey.data <- data.frame(metric = "satisfaction", likert.value.change = dialg.sys.data$post.satisfaction)
survey.data <- rbind(survey.data, data.frame(metric = "interest level", likert.value.change = dialg.sys.data$post.interest.level))
survey.data <- rbind(survey.data, data.frame(metric = "asr confidence", likert.value.change = dialg.sys.data$post.asr.confidence))
survey.data <- rbind(survey.data, data.frame(metric = "ease of use", likert.value.change = dialg.sys.data$post.ease.of.use))
survey.data <- rbind(survey.data, data.frame(metric = "previous experience", likert.value.change = dialg.sys.data$post.previous.experience))
ggplot(survey.data, aes(x = likert.value.change, fill = metric)) + geom_density(alpha=.3) + 
  xlab("Likert Scale Value") +
  ylab("Density") +
  ggtitle("Density Plot of Post-Use Survey")  + theme(legend.text=element_text(size=12))


# Density plots of survey outcome shift
survey.data <- data.frame(metric = "satisfaction", likert.value.change = dialg.sys.data$satisfaction)
survey.data <- rbind(survey.data, data.frame(metric = "interest level", likert.value.change = dialg.sys.data$interest.level))
survey.data <- rbind(survey.data, data.frame(metric = "asr confidence", likert.value.change = dialg.sys.data$asr.confidence))
survey.data <- rbind(survey.data, data.frame(metric = "ease of use", likert.value.change = dialg.sys.data$ease.of.use))
survey.data <- rbind(survey.data, data.frame(metric = "previous experience", likert.value.change = dialg.sys.data$previous.experience))
ggplot(survey.data, aes(x = likert.value.change, fill = metric)) + geom_density(alpha=.3) +
  xlab("Likert Scale Value Change (Post - Pre)") +
  ylab("Density") +
  ggtitle("Density Plot of Pre-/Post-Survey Differences") + theme(legend.text=element_text(size=12))

