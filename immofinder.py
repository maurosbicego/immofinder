import requests as r
import json
import time
import urllib
import argparse
import datetime
from datetime import datetime,timedelta
from simplejson.errors import JSONDecodeError
f = open('config.json')
config = json.load(f)

locationkeys = []
targetDurations = {}
for location in config["locations"]:
    locationkeys.append(location["id"])
    targetDurations[location["id"]] = location["maxDuration"]

def getLocationId(searchTerm):
    location = r.get("https://rest-api.immoscout24.ch/v4/de/locations?term={}".format(searchTerm)).json()[0]
    id = location['id']
    return id

def getDurations(lat,long):
    arrivaltimes = r.post("https://rest-api.immoscout24.ch/v4/de/services/commuting/arrivalsearches", json={"from":[{"id":"0","coords":{"lat":lat,"lng":long}}],"to":config["locations"]}).json()
    durations = {arrivaltimes[0]["to"][0]['id']:arrivaltimes[0]["to"][0]["transportations"][0]["travelTime"], arrivaltimes[0]["to"][1]['id']:arrivaltimes[0]["to"][1]["transportations"][0]["travelTime"]}
    return durations

s_params = {"Haus/Wohnung":1,"Wohnung":2,"Haus":3}
t_params = {"Mieten":1,"Kaufen":2}
search_available_earliest = datetime.fromisoformat(config["earliestAvailability"])

options = {
    "s":config["s"],
    "t":config["t"],
    "pf":config["priceFrom"],
    "pt":config["priceTo"],
    "nrf":config["roomNumberMin"],
    "nrt":config["roomNumberMax"],
    "r":config["range"]
}




locationId = getLocationId(config["location"])
params = "l={}&{}&inp=1".format(locationId,urllib.parse.urlencode(options))
resultCount = r.get("https://rest-api.immoscout24.ch/v4/de/properties/searchmetadata?{}".format(params)).json()['totalMatches']
resultSet = r.get("https://rest-api.immoscout24.ch/v4/de/properties?{}".format(params), headers={"is24-meta-pagesize":str(resultCount)}).json()
properties = resultSet['properties']
for propertyObj in properties:
    try:
        response = r.get("https://rest-api.immoscout24.ch/v4/de/properties/{}".format(propertyObj['id']))
        fullDetails = response.json()['propertyDetails']
        if "description" in fullDetails:
            reachable = True
            if any(keyword.lower() in fullDetails['description'].lower() for keyword in config["searchKeywords"]) or (len(config["searchKeywords"]) == 0):
                durations = {}
                for location in locationkeys:
                    duration = getDurations(propertyObj['latitude'],propertyObj['longitude'])[location]
                    durations[location] = duration
                    reachable = reachable and (duration <= targetDurations[location])
                if reachable:
                    try:
                        availableFrom = datetime.fromisoformat(propertyObj["availableFrom"])
                    except:
                        availableFrom = "Not defined!"
                    if type(availableFrom) == str or (availableFrom-search_available_earliest).total_seconds() > 0:
                        print(fullDetails['description'])
                        for location in locationkeys:
                            print("Duration to {}: {}".format(location, str(timedelta(seconds=durations[location]))))
                        print("Available from: {}".format(availableFrom))
                        print("Price: {}".format(propertyObj['price']))
                        print("https://www.immoscout24.ch{}".format(propertyObj["propertyUrl"]))
                        print("\n\n\n\n\n")
                        print("------------------------------------------------------------------------------")
                        print("\n\n\n")
        time.sleep(1)
    except JSONDecodeError:
        print("No valid JSON-Response was returned")
        if "rest-api.immoscout24.ch needs to review the security of your connection before proceeding" in response.text:
            time.sleep(10)
        