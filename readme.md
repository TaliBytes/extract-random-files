# Introduction

A simple python script that requests a dir from which to "extract" (copy) random files from. A target threshold (in GB) is also requested. This project was created to quickly extract x GBs of images/videos for a digital picture frame. The media needed to be randomly selected to provide a good sampling from over the years.

## How It Works

###

#### Run Script

Run the extract-random-files Python3 script in a terminal.

#### Initialization

User is prompted (via dialog box) for the number of GB of files to extract and a directory the extraction should begin in. If the directory is valid, the program initializes extraction (a while loop calling the selectItem() function.).

#### def selectItem

Loops through each entry in the user-provided dir. If it is a directory, it goes into it. If it is a file, it copies it to the /EXTRATED folder (which is created in the directory the extraction was initialized in).

#### Termination

The scripts self-terminates once either enough data is extracted OR it finds an empty directory too many times. Additionally, the upper limit of the GB to be extracted is automatically set to the same size of the directory the user begins the extraction in. Duplicates are avoided.

#### Once Extracted

Once all of the files are sorted, the CLI prints a messaged stating the sort has been completed.

## Contributions

This project is currently considered completed. However, I will still review pull requests if you strongly belive a feature should be added. Any features requested should be very simple in nature as to fit with the purpose of this script.
