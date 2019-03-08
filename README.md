# GrsChronoComp
GRSChronoComp is a tool set made in python, that can be used for analysis of time data. 

## chronPercentile
Its main purpose is to determine the time at which a certain percentage of the daily activity is reached. For this it takes in any of the formats created/provided by either the UK Biobank, the epochConversion script or the accelerometer feature creator script. It will work with whatever time steps are given in the document (UK Biobank, default 5s) and is therefore able to be used very flexibly.
The script takes four parameters ```[-w W][-t][-o [out]][-p [precision]] IL percentiles [percentiles]``` where the precision if unspecified is 10% and the results will be printed to the console if no file is specified with -o. IL specifies, where the data should be taken from, this can be a single file, a directory or a list of file in plain text format. The percentages of interest will be entered in percentiles as floating point values, where 1 = 100% and 0 = 0% or as values in the range 1-100. All values will be taken as their absolute value, so that negative values dont harm.
<br>
The output format is tab seperated with the complimentary columns ID and Date, where ID is either derived from the document name or file contents. Date is the date on which the measurement was taken. These two columns are then followed by an arbitrary number of percentages or times in a HH:MM:SS format(depending on the -t flag), in the order they were specified in the script call.
<br>
A new feature, the -w argument allows to add in a file contaning the awaken hours of a person. If it is added, the calculated times and percentages will only refer  to the "awake" part of the day. Meaning, only activity during those hours is considered. Times are still based on the 24 hour clock of the standard day and will wrap around for a new day, in case the go-to-sleep time is past midnight. The percentages are based on the relation of time to waken time (-> (currentTime-StartTime)/(EndTime-StartTime)).
The file in which the wake data is stored must follow the standard outlined by Dr. Andrew Woods file

## dayPercentage 
This is a small script to change data generate with chronPercentile from a HH:MM:SS format into a daypercentage or seconds since day start. it does not offer the same results as chronPercentile does, when used with a wake file, as it does not support it. 
USAGE: ```inlis [-o O] [-p [P]``` where inlis is the file or the direcotry of chronPercentile Data -o is the outputfile and -p is the number of digits for the conversion into a percentage, which by default is 5.
