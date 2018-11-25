from datetime import date
import statistics

#returns a boolean value stating whether an anomaly was found
def workHistoryAnomaly(workHistory, targetSignifier):
    dateProcessing = None
    anomaly = False
    targetLocation = targetSignifier.index(1)
    startDateParse = []
    endDateParse = []
    tempArray = []
    days = []
    
    for x in workHistory:
        dateProcessing = x.split('-')
        dateParse = dateProcessing[0].split(' ')

        startDateParse.append(dateParse[0])
        startDateParse.append(dateParse[1])
        endDateParse.append(dateParse[3])
        endDateParse.append(dateParse[4])

        tempArray = dateParser(startDateParse)
        startDate = date(tempArray[0], tempArray[1], tempArray[2])
        tempArray = []

        tempArray = dateParser(endDateParse)
        endDate = date(tempArray[0], tempArray[1], tempArray[2])

        days.append(abs(endDate-startDate).days)
        
        startDateParse = []
        endDateParse = []
    
    targetDays = days[targetLocation]
    del days[targetLocation]
    average = sum(days)/len(days)
    stdDev = statistics.stdev(days)
    threshold = average - stdDev
    if targetDays < threshold :
        anomaly = True

    return anomaly

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
    testData = ["Oct 1990 – Jun 1995", "Jun 1995 – Aug 2000", "Aug 2000 – May 2005", "May 2005 – Jul 2010", "Jul 2010 – Sept 2011"]
    testSignifier = [0,0,0,0,1]

    print(workHistoryAnomaly(testData,testSignifier))