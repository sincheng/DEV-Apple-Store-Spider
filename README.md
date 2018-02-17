# DEV-Apple-Store-Spider
Create a spider with Scrapy to scrape Apple store information including Store image, name, address and regions...etc from website (Link: https://www.apple.com/retail/storelist/)

## Prerequisites
Libraries need to be used in this program

1. Scrapy</br>
To build a spider project
```
$ pip install scrapy
import scrapy
```
2. Httplib2</br>
To connect google map API
```
$ pip install httplib2
import httplib2
```
3. OS</br>
Call the GOOGLE_API_KEY which is stored as environment variable for security
```
import os
```
4. JSON</br>
Parse json from google map api result 
```
import json
```

## Functions
This spider project contains 4 functions including 2 parse functions
</br>
#### stores.py 
##### parse(self,response) 
The function extracts the country , region and city fields of each store and extract store address to further scraping 
##### parse_store(self,response)
Second parse function to extract Store name , address , img url and coordinates.
##### findAddress(inputString)
A function to extract address from response and return as string</br>
#### geocode.py
##### getCoordinates(inputSting)
A function to connect google map api and get the coordinates of the address

## Testing
working on it, will update soon

## Output

