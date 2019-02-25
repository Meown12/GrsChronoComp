import argparse
import os
#import epochConv
import datetime

ALLOWED_EXTENSIONS = (".tsv")
HEADER_COLUMNS = 2
DAYSECONDS = (24* 3600)
PRECISION = 8
BUFFERLENGTH = 10000


def convertLine(line, precision = PRECISION):
    """
    Takes a single line of the input and converts given time values outside the header column into a percentage of the day.
    :param line: text line with the amount of heade columns specified in HEADER_COLUMNS and time in the format HH:MM:SS, seperated by tab
    :param precision: number of decimal place to round to, when converting
    :return: line, as before but with the times replaced with the corresponding percentage of the day
    """
    lineParts = line.strip().split("\t")
    outLine = ""
    fractionCounter = 0
    for fraction in lineParts:
        # two columns are always to be copied
        if fractionCounter < HEADER_COLUMNS:
            if outLine == "":
                outLine += fraction
            else:
                outLine += "\t" + fraction
        else: # normal time

            try:
                fractioDT = datetime.datetime.strptime(fraction, "%H:%M:%S")
                fractionTime = fractioDT.time()
                seconds = fractionTime.hour*3600+ fractionTime.minute*60 + fractionTime.second
                percent = seconds /DAYSECONDS                                                   # to get seconds change here to : seconds + "/" + DAYSECONDS
            except ValueError:
                return ""
            outLine += "\t{}".format(round(percent,precision))                                  # to get seconds change here to : outLine += "\t" + percent

        fractionCounter += 1
    outLine += "\n"
    return outLine

def convertPercentages(infile, outfile = "", precision = PRECISION):
    """
    Function that converts a whole chronPercentile file from time into
    :param infile: file path to a file created with chron percentile
    :param outfile: path the changed file should be saved to
    :param precision: precision of the float conversion of the percentage calculation
    """
    with open(infile, "r") as inFile:
        lineCount = 0
        outLine = ""
        start = True
        for line in inFile:
            lineCount += 1
            # one header line, that should be written straight away
            if not start:
                # normal line
                outLine += convertLine(line, precision)
            else:
                outLine = line
                start = False
            if outfile != "":
                if lineCount > BUFFERLENGTH:
                    with open(outfile, "a") as outFile :
                        outFile.write(outLine)
                    lineCount = 0
                    outLine = ""
            else:
                print(outLine)
    if outfile != "": # final leftover save
        with open(outfile, "a") as outFile:
            outFile.write(outLine)

def main():
    """
    The main function for the time to percentage conversion script.
    :return: none
    """
    # takes accelerometer file (both formats) or directory,
    parser = argparse.ArgumentParser(description="Script to change times to day percentages")
    parser.add_argument("inlis", metavar="IL",  help="Location of a file or a directory to be read")
    parser.add_argument("-o", nargs="?", type=str, dest="out", const="", help="output location")
    parser.add_argument("-p", nargs="?", type=int, dest="precision", const="5", help="number of decimal places for the output")
    args = parser.parse_args()
    fileList = []
    # check percentage level input
    percentages = []
    if os.path.isfile(os.path.abspath(args.inlis)) and args.inlis.endswith(ALLOWED_EXTENSIONS):
        # only one file to look at
        fileList.append(os.path.abspath(args.inlis))
    else: # a directory or file list
       #  fileList = epochConv.getFiles(args.inlis)
        print("cant do on cook due to pytz missing, reenable once available")
    try:
        os.remove(os.path.abspath(args.out))
    except:
        pass
    #calculate results
    for fileName in fileList:
        resultString= convertPercentages(fileName, args.out, args.precision)

if __name__ == "__main__":
    main()