from datetime import date
import datetime
import statistics
from urllib.parse import unquote

#returns a string with the output
def workHistoryAnalyser(workHistory):
    workHistory = unquote(workHistory)
    dateProcessing = None
    startDateParse = []
    endDateParse = []
    tempArray = []
    days = []
    
    for x in workHistory:
        dateProcessing = x.split('-')
        dateParse = dateProcessing[0].split(' ')

        startDateParse.append(dateParse[0])
        startDateParse.append(dateParse[1])
        if len(dateParse) > 4:
            endDateParse.append(dateParse[3])
            endDateParse.append(dateParse[4])
        else:
            endDateParse.append(dateParse[3])

        tempArray = dateParser(startDateParse)
        startDate = date(tempArray[0], tempArray[1], tempArray[2])
        tempArray = []

        if len(dateParse) > 4:
            tempArray = dateParser(endDateParse)
            endDate = date(tempArray[0], tempArray[1], tempArray[2])
        else:
            tempEndDate = datetime.datetime.now()
            endDate = date(int(tempEndDate.year), int(tempEndDate.month), int(tempEndDate.day))

        days.append(abs(endDate-startDate).days)
        
        startDateParse = []
        endDateParse = []
    
    average = sum(days)/len(days)
    stdDev = statistics.stdev(days)
    
    isAnomalous = average - stdDev
    anomalousPos = []
    count = 0

    for y in days:
        if (y < isAnomalous):
            anomalousPos.append(count)
        count += 1

    returnString = """{
	"items": [{
		"averageDaysWorked": "%s",
		"stdDev": "%s",
        "anomalies": [""" % (str(average),str(stdDev))

    for z in anomalousPos:
        returnString += """{ "index": "%s", "days": "%s"},""" % (str(z),str(days[z]))

    if returnString[-1] == ",":
        returnString = returnString[:-1]
    returnString += """]}]}"""
    print(returnString)

    return returnString

def dateParser(date):
    #Year, Month, Day
    returnArray = [0,0,1]
    if date[0] == 'Jan':
        returnArray[1] = 1
    elif date[0] == 'Feb':
        returnArray[1] = 2 
    elif date[0] == 'Mar':
        returnArray[1] = 3 
    elif date[0] == 'Apr':
        returnArray[1] = 4 
    elif date[0] == 'May':
        returnArray[1] = 5 
    elif date[0] == 'Jun':
        returnArray[1] = 6 
    elif date[0] == 'Jul':
        returnArray[1] = 7 
    elif date[0] == 'Aug':
        returnArray[1] = 8 
    elif date[0] == 'Sept' or date[0] == 'Sep':
        returnArray[1] = 9 
    elif date[0] == 'Oct':
        returnArray[1] = 10 
    elif date[0] == 'Nov':
        returnArray[1] = 11 
    elif date[0] == 'Dec':
        returnArray[1] = 12

    returnArray[0] = int(date[1]) 
    return returnArray


if __name__ == '__main__':
    testData = ["Jan 2007 – Nov 2010", "Nov 2010 – Oct 2014", "Oct 2014 – Jun 2018", "Jun 2018 – Aug 2018", "Aug 2018 – Present"]

    workHistoryAnalyser(testData)