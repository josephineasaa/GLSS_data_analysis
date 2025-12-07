library(haven)
library(foreign)
library(rio)
library(readr)

folder_paths <- c("2005 with csvs/aggregates","2005 with csvs/parta", "2005 with csvs/section10", "1991-1992/aggreg",  
                  "1991-1992/Prices", "1998/aggreg", "1998/Prices","2012-2013/AGGREGATES", "2012-2013/PARTA", "2012-2013/PRICES", 
                  "2017/g7aggregates", "2017/g7PartA", "2017/g7price")

for (folder in folder_paths) {
  if (!dir.exists(folder)) {
    message(paste("Skipping: Folder does not exist -", folder))
    flush.console()
    next
  }

  csv_folder <- paste0(folder, "_csv")
  dir.create(csv_folder, recursive = TRUE, showWarnings = FALSE)

  all_files <- list.files(folder, full.names = TRUE)
  valid_extensions <- c("sav", "dta")
  data_files <- all_files[tolower(tools::file_ext(all_files)) %in% valid_extensions]

  if (length(data_files) == 0) {
    message(paste("No .sav or .dta files found in", folder))
    flush.console()
    next
  }

  for (file in data_files) {
    data <- NULL  

    message(paste("Processing:", file))
    flush.console()

    file_ext <- tolower(tools::file_ext(file))

    if (file_ext == "sav") {
      tryCatch({
        message(paste("Trying haven for", file))
        flush.console()
        data <- read_sav(file, user_na = TRUE)
      }, error = function(e) {
        message(paste("Haven failed for", file, "-", e$message))
        flush.console()
      })

      if (is.null(data) || nrow(data) == 0) {
        tryCatch({
          message(paste("Trying foreign for", file))
          flush.console()
          data <- read.spss(file, to.data.frame = TRUE, use.value.labels = FALSE)
        }, error = function(e) {
          message(paste("Foreign failed for", file, "-", e$message))
          flush.console()
        })
      }
    }

    if (file_ext == "dta") {
      tryCatch({
        message(paste("Trying haven for", file))
        flush.console()
        data <- read_dta(file)
      }, error = function(e) {
        message(paste("Haven failed for", file, "-", e$message))
        flush.console()
      })
    }

    if (is.null(data) || nrow(data) == 0) {
      tryCatch({
        message(paste("Trying rio for", file))
        flush.console()
        data <- import(file)
      }, error = function(e) {
        message(paste("Rio failed for", file, "-", e$message))
        flush.console()
      })
    }

    if (is.null(data) || nrow(data) == 0) {
      message(paste("Skipping: No data found in", file))
      flush.console()
      next
    }

    print(head(data))
    flush.console()

    csv_file <- file.path(csv_folder, paste0(tools::file_path_sans_ext(basename(file)), ".csv"))
    write_csv(data, csv_file)

    message(paste("Successfully converted:", file, "->", csv_file))
    flush.console()
  }
}

message("All files processed.")
flush.console()
