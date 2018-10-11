#returns an array with anomaly to employees who quit ratio at position 0
#and employees who quit to total employees ratio at position 1
def workHistoryAnalyzer(anomalies,pastE,currentE):
    returnArray = []
    APR = anomalies/pastE
    totalE = pastE + currentE
    PTR = pastE/totalE

    returnArray.append(APR)
    returnArray.append(PTR)
    
    return returnArray

#testA = 7
#testP = 23
#testC = 130
#print(workHistoryAnalyzer(testA,testP,testC))