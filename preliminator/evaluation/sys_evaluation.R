# Placeholder script for system evaluation

# Load necessary packages
library(RJSONIO)
library(RCurl)
library(MASS)
library(leaps)

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
                             avg.user.word.len = numeric(0))
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
                     previous.experience , data = dialg.sys.data)
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
                            previous.experience , data = dialg.sys.data, nbest = 3)
#summary(fit.leaps)
plot(fit.leaps, scale = "r2")
