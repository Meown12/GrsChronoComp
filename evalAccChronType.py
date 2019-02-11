"""
This script should determine whether a person is more a morning or evening chronotype
For this it takes the accelFeature output and uses the hourly data
"""
import os
EXPECTED_HEADER = "ID\tDate\tDay Of The Week\tMean (mg)\tStandard Deviation (mg)\tMedian (mg)\tQ1 (mg)\tQ3 (mg)\t" \
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



def readData(filePath):
    """

    :param filePath:
    :return:
    """
    data = {}
    if "tsv" not in os.path.splitext(filePath)[1]:
        raise AttributeError("Wrong file format. Expecting .tsv, found {} .  Please change input!".format(
            os.path.splitext(filePath)[1]))

    with open(filePath, "r+")as featureData:
        # check correct file contents
        header = featureData.readline()
        if not (EXPECTED_HEADER == header):
            # basics dont seem to be fullfilled
            raise AttributeError("File seems to not fullfill the basic standards expected. (HEADER error)")

        for line in featureData:
            # read all accelData
            values = line.split("\t")
            #check for expected length of data row
            if len(values) != 128:
                continue
            id =  values[0]
            if id not in data:
                data[id] = [].append(values[1:])
            else:
                data[id] = data[id].append(values[1:])

def hourSetAvg(startHour, endHour, dataSet):

def hourSetSpike(startHour, endHour, dataSet):

def hourSetLow(startHour, endHour, dataSet):

def hourSetData(startHour, endHour, dataSet):
    # 7th field is Hour 0 and

def evalChrono(dataSet):


if __name__ == "__main__":
