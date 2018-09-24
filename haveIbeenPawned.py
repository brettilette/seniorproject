import requests
def haveIBeenPawned(emailAddress = ''):
	endPoint = 'https://haveibeenpwned.com/api/v2/breachedaccount/'
	response = requests.get(endPoint+emailAddress)
	output = response.json()
	return output

res = haveIBeenPawned('marcolcal@gmail.com')
print(res)
