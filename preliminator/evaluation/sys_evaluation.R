# Placeholder script for system evaluation

# Load necessary packages
library(RJSONIO)
library(RCurl)

# Import data from json files
for(file in dir()[grep(".json", dir())]) {
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
transcript <- transcript[which(transcript$interview >= transcript.limit),]

# Extract relevant susbset of pre-/post-surveys
presurvey <- presurvey[(nrow(presurvey) - tail.len + 1):nrow(presurvey),]
postsurvey <- postsurvey[(nrow(postsurvey) - tail.len + 1):nrow(postsurvey),]

# Set global statistics
sample.size <- nrow(candidate)


# Find best predictor of user satisfaction
