# Placeholder script for system evaluation

# Load necessary packages
library(RJSONIO)
library(RCurl)

# Import data from json files
for(file in dir()[grep(".json", dir())]) {
  # Strip file tag
  file.name <- gsub(".json", "", file)
  
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
  if (transcript[row, "line_number"] == 0) {
    curr_interview <- curr_interview + 1
  }
  transcript[row, "interview"] <- curr_interview
}




# Find best predictor of user satisfaction
