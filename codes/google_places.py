
##### Global Imports ####
import pandas
import requests
import time
import urllib
import sys

####### Near By Search API ########
start = int(sys.argv[1])
end = int(sys.argv[2])
apiKey = sys.argv[3]

def radar_search(lat, lng, radius,apiKey, types):
    # making the url
    AUTH_KEY = apiKey
    LOCATION = str(lat) + "," + str(lng)
    RADIUS = radius
    TYPES = types
    KEYWORD = types
    MyUrl = ('https://maps.googleapis.com/maps/api/place/radarsearch/json'
             '?location=%s'
             '&radius=%s'
             '&types=%s'
             '&key=%s'
             '&keyword=%s') % (LOCATION,RADIUS, TYPES, AUTH_KEY,KEYWORD)
    #print (MyUrl)
    response = requests.get(MyUrl)
    jsonData = response.json()
    return jsonData

def extractData(search):
    countTemp =0
    if search['status'] == 'OK':  # loop through results
        results = search['results']
        countTemp = len(search['results'])
    return countTemp


def nearBySearch(lat,lng,radius,typ,apiKey):
    search = radar_search(lat, lng, radius, apiKey,types=typ)
    count = 0
    count= extractData(search)
    return count



##### Iterating Over DataFrame ###
data = pandas.read_csv("post_code_details.csv")

#### Types Dict ####
typesDict = {'airport-10000': 10000,
 'atm-500': 500,
 'bank-500': 500,
 'bus_station-500': 500,
 'church-500': 500,
 'hospital-500': 500,
 'liquor_store-500': 500,
 'park-500': 500,
 'parking-500': 500,
 'pharmacy-500': 500,
 'police-500': 500,
 'restaurant-500': 500,
 'school-500': 500,
 'taxi_stand-2000': 2000,
 'train_station-1000': 1000,
 'university-500': 500
}


startNum = start
endNum = end-1
finalList = []
missedList = []
start_time = time.time()
print ("Start Time",start_time)
for line in data[start:end].itertuples():
    if line[0]%50==0: print (str(startNum) + "_" + str(endNum),"     ",line[0])
    try:
        latLongDict = {}
        for typ,radius in typesDict.items():
            #print(typ,radius)
            latLongDict[typ]=nearBySearch(line[2],line[3],radius,typ.split("-")[0],apiKey)
        finalList.append(latLongDict)
    except:
        missedList.append(line[1])
print("Time Take For Given Run %s seconds" % (time.time() - start_time))


finalDataFrame = pandas.DataFrame(finalList)
missedDataFrame = pandas.DataFrame(missedList,columns=["missed_post_code"])
finalDataFrame.to_csv(str(startNum) + "_" + str(endNum) + ".csv",index=False)
missedDataFrame.to_csv(str(startNum) + "_" + str(endNum) + "_" + "missed.csv",index=False)
