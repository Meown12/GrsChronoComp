"""Script to determine the times, where a certain percentile of daily activity is reached"""

import argparse
import datetime
import os
import gzip
import epochConv
import copy

ALLOWED_EXTENSIONS = (".csv.gz", ".csv", ".tsv")
ACCELFEAT_HEADER = "ID\tDate\tDay Of The Week\tMean (mg)\tStandard Deviation (mg)\tMedian (mg)\tQ1 (mg)\tQ3 (mg)\t" \
                 "Mean HR00\tStandard Deviation HR00\tMedian HR00\tQ1 HR00\tQ3 HR00\t" \
                 "Mean HR01\tStandard Deviation HR01\tMedian HR01\tQ1 HR01\tQ3 HR01\t" \
                 "Mean HR02\tStandard Deviation HR02\tMedian HR02\tQ1 HR02\tQ3 HR02\t" \
                 "Mean HR03\tStandard Deviation HR03\tMedian HR03\tQ1 HR03\tQ3 HR03\t" \
                 "Mean HR04\tStandard Deviation HR04\tMedian HR04\tQ1 HR04\tQ3 HR04\t" \
                 "Mean HR05\tStandard Deviation HR05\tMedian HR05\tQ1 HR05\tQ3 HR05\t" \
                 "Mean HR06\tStandard Deviation HR06\tMedian HR06\tQ1 HR06\tQ3 HR06\t" \
                 "Mean HR07\tStandard Deviation HR07\tMedian HR07\tQ1 HR07\tQ3 HR07\t" \
                 "Mean HR08\tStandard Deviation HR08\tMedian HR08\tQ1 HR08\tQ3 HR08\t" \
                 "Mean HR09\tStandard Deviation HR09\tMedian HR09\tQ1 HR09\tQ3 HR09\t" \
                 "Mean HR10\tStandard Deviation HR10\tMedian HR10\tQ1 HR10\tQ3 HR10\t" \
                 "Mean HR11\tStandard Deviation HR11\tMedian HR11\tQ1 HR11\tQ3 HR11\t" \
                 "Mean HR12\tStandard Deviation HR12\tMedian HR12\tQ1 HR12\tQ3 HR12\t" \
                 "Mean HR13\tStandard Deviation HR13\tMedian HR13\tQ1 HR13\tQ3 HR13\t" \
                 "Mean HR14\tStandard Deviation HR14\tMedian HR14\tQ1 HR14\tQ3 HR14\t" \
                 "Mean HR15\tStandard Deviation HR15\tMedian HR15\tQ1 HR15\tQ3 HR15\t" \
                 "Mean HR16\tStandard Deviation HR16\tMedian HR16\tQ1 HR16\tQ3 HR16\t" \
                 "Mean HR17\tStandard Deviation HR17\tMedian HR17\tQ1 HR17\tQ3 HR17\t" \
                 "Mean HR18\tStandard Deviation HR18\tMedian HR18\tQ1 HR18\tQ3 HR18\t" \
                 "Mean HR19\tStandard Deviation HR19\tMedian HR19\tQ1 HR19\tQ3 HR19\t" \
                 "Mean HR20\tStandard Deviation HR20\tMedian HR20\tQ1 HR20\tQ3 HR20\t" \
                 "Mean HR21\tStandard Deviation HR21\tMedian HR21\tQ1 HR21\tQ3 HR21\t" \
                 "Mean HR22\tStandard Deviation HR22\tMedian HR22\tQ1 HR22\tQ3 HR22\t" \
                 "Mean HR23\tStandard Deviation HR23\tMedian HR23\tQ1 HR23\tQ3 HR23\t" \
                 "Daylight Savings\n"

def chronPercentileDay(dayData, percentileList, precision):
    """
    Calculates percentiles for a given Day.
    dayData should be given as a two dimensional array with the time as a datetime object and the accelerometer average for that period.
    It also takes a list of percentiles for which the times should be given.
    """
    result = ["NA" for i in range(len(percentileList))]
    daySum = sum(dayData[1])
    currentSum = 0
    offsets =  [percentileList,
                [0 for i in range(len(percentileList))],
                [ 1 for i in range(len(percentileList))],
                [ None  for i in range(len(percentileList))]]
        # stores the index closest to the required percentage and its distance and time-> required percent, ind, distance, time
    for n in range(len(dayData[1])):
        # for every datapoint check whether a percentile is reached, and save the time
        currentSum += dayData[1][n]
        percent = currentSum / daySum
        for j in range(len(percentileList)):
            # check for all percentages
            distance = abs(percent - percentileList[j])
            if distance < precision and distance < offsets[2][j]:
                offsets[3][j] = dayData[0][n]   # time
                offsets[2][j] = distance        # distance
                offsets[1][j] = n               # index
    for k in range(len(offsets[0])):
        if  offsets[3][k] != None:
            result[k] = offsets[3][k]
    return result


def readData(fileName):
    # there can be three types of files this script can operate with, original 5 second data, processed raw Data and feature data
    results = None
    if not fileName.endswith(ALLOWED_EXTENSIONS) :
        raise AttributeError("Wrong file format. Expecting {}, found {} .  Please change input!".format(
            ALLOWED_EXTENSIONS,
            os.path.splitext(fileName)[1]))
    compressed = False
    try: # opening the file
        if os.path.splitext(fileName)[1] == ".gz":
            #compressed data, check if raw data
            datFile = gzip.open(fileName, "rt")
            compressed = True
        else:
            # not compressed so maybe not raw data
            datFile = open(fileName, "r")
    except IOError:
        print("Could not open file {}".format(fileName))
        return None

    try: # reading the file
        # check correct file contents
        header = datFile.readline()
        if (ACCELFEAT_HEADER == header):
            results = readAccelFeatureData(datFile)

        elif "Measurement from" in header:
            #processed data
            results= readProcessedData(datFile)
        elif header.startswith("acceleration"):
            # raw data
            results= readRawData(datFile)
    finally:
        datFile.close()
    return results



def readRawData(file):
    """
    To use to read raw data files into the chronPercentile Script
    :param file: file object from where to read the data
    :return:
    """
    results = [[],[]]
    result = [[],[]]
    file.seek(0)
    header = file.readline()
    offset = 0
    currentTime = None
    oldTime = None
    for line in file:
        oldTime = currentTime
        offset += 1
        currentTime = epochConv.getTimeStampDT(header, offset, 5)
        if  (oldTime != None) and (currentTime.day != oldTime.day):
            results[0].append((os.path.basename(file.name)).split(".")[0])
            results[1].append(copy.deepcopy(result))
            result[0].clear()
            result[1].clear()
        result[0].append(currentTime)
        result[1].append(float(line.split(",")[0]))
    results[0].append((os.path.basename(file.name)).split(".")[0])
    results[1].append(copy.deepcopy(result))
    result[0].clear()
    result[1].clear()
    return results



def readProcessedData(file):

    results = [[],[]]
    result = [[],[]]
    next(file) # skip the header line, if not done so already
    i = 0 # day index
    oldTime = None
    currentTime = None
    for line in file:
        lineParts =line.strip().split("\t")
        if len(lineParts) == 3 and lineParts[1] != -1:
            oldTime = currentTime
            currentTime = datetime.datetime.strptime(lineParts[0], "%Y-%m-%dT%H:%M:%S")
            if oldTime != None and currentTime.day != oldTime.day:
                results[0].append((os.path.basename(file.name)).split(".")[0])
                results[1].append(copy.deepcopy(result))
                result[0].clear()
                result[1].clear()
            result[0].append(currentTime)
            result[1].append(float(lineParts[1]))
        else:
            # line incomplete, discard
            pass
    results[0].append((os.path.basename(file.name)).split(".")[0])
    results[1].append(copy.deepcopy(result))
    result[0].clear()
    result[1].clear()
    return results

def readAccelFeatureData(file):
    # only the mean is interesting, so load that
    # 8 + 5*n columns until n = 23
    # date column is the second from the left with YYYY-mm-dd
    results = [[],[]]
    result = [[],[]]
    i = 0
    next(file)
    for line in file:
        # each line is a new day
        i += 1
        line = line.strip().split("\t")
        date = line[1].split("-")
        for n in range(0,24):
            if (line[8 + 5 * n] != "N/A"):
                result[0].append(datetime.datetime(year=int(date[0]), month=int(date[1]), day= int(date[2]),hour= n, minute= 0, second= 0))
                result[1].append(float(line[8+5*n]))
        results[0].append(line[0])
        results[1].append(copy.deepcopy(result))
        result[0].clear()
        result[1].clear()
    return results




def main():
    # takes accelerometer file (both formats) or directory,
    parser = argparse.ArgumentParser(description="Script to determine  the times, where a certain percentile of "
                                                 "daily activity is reached")
    parser.add_argument("inlis", metavar="IL",  help="Location of a file or a directory to be read")
    parser.add_argument("pargs", nargs="+", type=float, help="Percentiles to be analyzed" )
    parser.add_argument("-o", nargs="?", type=str, dest="out", const="", help="output location")
    parser.add_argument("-p", nargs="?", type=float, dest="precision", const="0.05", help="precision for time approximation")
    args = parser.parse_args()
    fileList = []
    precision = args.precision if args.precision != None else 0.05
    # check percentage level input
    percentages = []
    for value in args.pargs: # values need to be between 0 and 1, so we may need to convert them.
        if float(value) > 1: # assume XX.XX... [%] writing, divide by 100
            percentages.append(round(abs(float(value))/100, 8))
        else:
            percentages.append(round(abs(float(value)), 8))

    if os.path.isfile(os.path.abspath(args.inlis)) and args.inlis.endswith(ALLOWED_EXTENSIONS):
        # only one file to look at
        fileList.append(os.path.abspath(args.inlis))
    else: # a directory or file list
        fileList = epochConv.getFiles(args.inlis)

    results = [[],[],[]]
    for fileName in fileList:
        data = readData(fileName)

        for i in range(len(data[0])):
            percentileResults = chronPercentileDay(data[1][i], percentages, precision) # give it one day of data
            results[0].append(data[0][i]) # add id
            results[1].append(data[1][i][0][0].strftime("%Y-%m-%d")) # append date from the first element in the data set
            results[2].append(percentileResults)

    # output
    # write header
    outText = ""
    outText += "ID\tDate"
    for percentage in percentages:
        outText += "\t{}".format(percentage)
    outText += "\n"
    # write data
    for i in range(len(results[0])):
        # for every day dataset
        outText += ("{}\t{}".format(results[0][i], results[1][i]))
        for percentage in results[2][i]:
            outText += ("\t{}".format((datetime.datetime.strftime(percentage, "%H:%M:%S"))if percentage != "NA" else "lacking Data"))
        outText += ("\n")

    if args.out != None: # we need to save
        with open(os.path.abspath(args.out), "w") as outFile:
            outFile.write(outText)
    else:
        print(outText)



            
if __name__ == "__main__":
    main()