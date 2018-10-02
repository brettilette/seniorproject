from datetime import date
import statistics

#returns an array with the average at 0 and the stdDev at 1
def workHistoryAnalyser(workHistory):
    dateProcessing = None
    startDateParse = None
    endDateParse = None
    tempArray = []
    days = []
    returnArray = []
    
    for x in workHistory:
        dateProcessing = x.split('-')
        startDateParse = dateProcessing[0].split(' ')
        endDateParse = dateProcessing[1].split(' ')

        tempArray = dateParser(startDateParse)
        startDate = date(tempArray[0], tempArray[1], tempArray[2])
        tempArray = []

        tempArray = dateParser(endDateParse)
        endDate = date(tempArray[0], tempArray[1], tempArray[2])

        days.append(abs(endDate-startDate).days)
    
    average = sum(days)/len(days)
    stdDev = statistics.stdev(days)
    returnArray.append(average)
    returnArray.append(stdDev)

    return returnArray

def dateParser(date):
    #Year, Month, Day
    returnArray = [0,0,1]
    if date[0] == 'Jan':
        returnArray[2] = 1
    elif date[0] == 'Feb':
        returnArray[2] = 2 
    elif date[0] == 'Mar':
        returnArray[2] = 3 
    elif date[0] == 'Apr':
        returnArray[2] = 4 
    elif date[0] == 'May':
        returnArray[2] = 5 
    elif date[0] == 'Jun':
        returnArray[2] = 6 
    elif date[0] == 'Jul':
        returnArray[2] = 7 
    elif date[0] == 'Aug':
        returnArray[2] = 8 
    elif date[0] == 'Sept' or date[0] == 'Sep':
        returnArray[2] = 9 
    elif date[0] == 'Oct':
        returnArray[2] = 10 
    elif date[0] == 'Nov':
        returnArray[2] = 11 
    elif date[0] == 'Dec':
        returnArray[2] = 12

    returnArray[0] == date[1] 
    return returnArray

