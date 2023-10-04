#import requests

#url = "https://worldtimeapi.org/api/timezone/America/New_York"
#reply = requests.get(url)
#print(reply)



#import requests

#url = "https://worldtimeapi.org/api/timezone/America/New_York"
#reply = requests.get(url)
#print(reply.json()['datetime'])


import requests

def GetIt(url,element):
    reply = requests.get(url)
    if reply.status_code == 200:
        return(reply.json()[element])
    else:
        return('Error')   

url = "https://worldtimeapi.org/api/timezone/America/Boulder"
fullTime = GetIt(url,'datetime')
myDate = fullTime.split('T')[0]  #get the date
myTime = fullTime.split('T')[1].split('.')[0]  #get the time
print(myDate)
print(myTime)