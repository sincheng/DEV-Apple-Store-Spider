import httplib2
import json
import os
import re

# Function to use Google Maps to convert a location into Latitute/Longitute coordinates
def getCoordinates(inputString):
    #Store Google api key as environemnt variable for security
    google_api_key = os.environ['GOOGLE_API_KEY']
    #Remove special characters
    locationString = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", " ", inputString)
    locationString = locationString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'% (locationString, google_api_key))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    #if no result find, will show NA
    latitude = "NA" if result ['status'] !="OK" else result['results'][0]['geometry']['location']['lat']
    longitude = "NA" if result ['status'] !="OK"  else result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)
