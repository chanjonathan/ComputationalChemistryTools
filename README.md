# Computational Chemistry Tools

A set of scripts that let you bypass the Gaussian GUI and instantly generate job files from given job keywords

## Introduction

For a computational chemist, submitting multiple jobs can done done easily with a shell script. The main bottleneck comes from being forced to use the Gaussian GUI, the generate these job files, one by one. This set of scripts is intended to help the chemists save time and increase their job throughput by creating the multiple job files at once all from the convenience of the command line.

These scripts can convert multiple .log files to .com files, extract multiple frames from multiple .sdf files and convert them to .com files, and lastly extract energy data from multiple .log files to csv format for use in spreasheets. 

## Installation

To be able execute script from anywhere:
 - Add the shebang line `#!/usr/bin/env python3` to the beginning of each script
 - Rename and remove the .py file extension
 - Move script to `/bin` or `~/bin`
 - Grant files executable permission

## Commands

### log2com
`log2com file.log` Converts specified .log file to .com file. Will prompt user to enter job keywords line.

`log2com -all` Converts all .log files in directory to .com files. Will prompt user to enter job keywords line.

### sdf2com
`sdf2com file.sdf` Converts specified .sdf file to .com file. Will prompt user to enter job keywords line.

`sdf2com -all` Converts all .sdf files in directory to .com files. Will prompt user to enter job keywords line.

### log2csv
`log2csv` Extracts data from all .log files in directory and saves then in a file named `energies.csv`.

## User Stories
### log2com
- As a user, I want to be able to specify the job keywords once for all the .com files to be generated
- As a user, I want to be able to target a specic .log file to be converted to a .com file
- As a user, I want to be able to target all .log files in a directory to be converted to .com files
- 
### sdf2com
- As a user, I want to be able to specify the job keywords once for all the .com files to be generated
- As a user, I want to be able to extract all the frames of an .sdf file for conversion to .com files
- As a user, I want to be able to target a specic .sdf file to be converted to a .com file
- As a user, I want to be able to target all .sdf files in a directory to be converted to .com files
- 
### log2csv
- As a user, I want to be able to extract energy data from all .log files in a directory and have it saved in csv format
