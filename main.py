# -*- coding: utf-8 -*-
"""Uber_reimburse

Automatically generated by Colab.

Uncomment below if using Colab, otherwise install libraries mentioned in comments
"""
#from google.colab import drive
#drive.mount('/content/drive')
#!pip install requests
#!pip install pandas
#!pip install weasyprint


import requests
import pandas as pd
from datetime import datetime
from dateutil import tz
from time import mktime

from weasyprint import HTML

import logging
logging.getLogger('weasyprint').setLevel(100)

# get UNIX millisecond timestamp for beginning and end of target month as m/d/yyyy
fromTime = int(str(int(datetime(2025, 2, 1,0,0,0).timestamp())) + '000')
toTime = int(str(int(datetime(2025, 2, 28,23,59,59).timestamp())) + '999')
## DOES it need to be in UTC/GMT or MOUNTAIN?? ### ANSWER: UTC/GMT otherwise the search cuts off evening end of month rides
# TODO: correct for if end of month is in the future, use current datetime
print(f"[DEBUG] Datetime: {fromTime} -> {toTime}")

api_url = 'https://riders.uber.com/graphql'
cursor = '0'
"""
Change the below path based on where you're running this script from.
"""
base_url = '/content/drive/MyDrive/uber-reimburse/'

# Click on api_url link, after logging in, click api_url again, F12 to get console, go to NETWORK tab and refresh, right-click on "graphql" and copy -> as cUrl.
# Past this into https://curlconverter.com/python/ and copy-paste "cookies" dict below
cookies = {
    'marketing_vistor_id': '<redacted>',
    'utag_main__sn': '1',
 
    # .... rest of cookie here
}



# Get list of RIDES in MONTH
def get_rides(fromTime, toTime, cursor='0', api_url='https://riders.uber.com/graphql', cookies=cookies):
  true = "true"
  headers = {
      'authority': 'riders.uber.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'sec-ch-prefers-color-scheme': 'light',
      'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'x-csrf-token': 'x',
  }

  json_data = {
      'operationName': 'GetTrips',
      'variables': {
          'cursor': cursor,
          'fromTime': fromTime,
          'toTime': toTime,
      },
      'query': 'query GetTrips($cursor: String, $fromTime: Float, $toTime: Float) {\n  getTrips(cursor: $cursor, fromTime: $fromTime, toTime: $toTime) {\n    count\n    pagingResult {\n      hasMore\n      nextCursor\n      __typename\n    }\n    reservations {\n      ...TripFragment\n      __typename\n    }\n    trips {\n      ...TripFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TripFragment on Trip {\n  beginTripTime\n  disableCanceling\n  driver\n  dropoffTime\n  fare\n  isRidepoolTrip\n  isScheduledRide\n  isSurgeTrip\n  isUberReserve\n  jobUUID\n  marketplace\n  paymentProfileUUID\n  status\n  uuid\n  vehicleDisplayName\n  waypoints\n  __typename\n}\n',
  }

  json_data = {
      "operationName":"Activities",
      "variables": {
          "orderTypes":["RIDES","TRAVEL"],
          "profileType":"BUSINESS",
          "endTimeMs": toTime,
          "startTimeMs": fromTime
        },
      "query":"query Activities($cityID: Int, $endTimeMs: Float, $nextPageToken: String, $orderTypes: [RVWebCommonActivityOrderType!] = [RIDES, TRAVEL], $profileType: RVWebCommonActivityProfileType = BUSINESS, $startTimeMs: Float) {\n  activities(cityID: $cityID) {\n    cityID\n    past(\n      endTimeMs: $endTimeMs\n        nextPageToken: $nextPageToken\n      orderTypes: $orderTypes\n      profileType: $profileType\n      startTimeMs: $startTimeMs\n    ) @include(if: TRUE) {\n      activities {\n        ...RVWebCommonActivityFragment\n        __typename\n      }\n      nextPageToken\n      __typename\n    }\n    upcoming @include(if: FALSE) {\n      activities {\n        ...RVWebCommonActivityFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment RVWebCommonActivityFragment on RVWebCommonActivity {\n  buttons {\n    isDefault\n    startEnhancerIcon\n    text\n    url\n    __typename\n  }\n  cardURL\n  description\n  imageURL {\n    light\n    dark\n    __typename\n  }\n  subtitle\n  title\n  uuid\n  __typename\n}\n"

  }

  json_data_v2 = {
  "operationName": "Activities",
  "variables": {
    "limit": 99,
    "orderTypes": [
      "RIDES",
      "TRAVEL"
    ],
    "profileType": "PERSONAL",
    "cityID": 24,
    "endTimeMs": toTime,
    "startTimeMs": fromTime
  },
  "query": "query Activities($cityID: Int, $endTimeMs: Float, $includePast: Boolean = true, $includeUpcoming: Boolean = true, $limit: Int = 5, $nextPageToken: String, $orderTypes: [RVWebCommonActivityOrderType!] = [RIDES, TRAVEL], $profileType: RVWebCommonActivityProfileType = PERSONAL, $startTimeMs: Float) {\n  activities(cityID: $cityID) {\n    cityID\n    past(\n      endTimeMs: $endTimeMs\n      limit: $limit\n      nextPageToken: $nextPageToken\n      orderTypes: $orderTypes\n      profileType: $profileType\n      startTimeMs: $startTimeMs\n    ) @include(if: $includePast) {\n      activities {\n        ...RVWebCommonActivityFragment\n        __typename\n      }\n      nextPageToken\n      __typename\n    }\n    upcoming @include(if: $includeUpcoming) {\n      activities {\n        ...RVWebCommonActivityFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment RVWebCommonActivityFragment on RVWebCommonActivity {\n  buttons {\n    isDefault\n    startEnhancerIcon\n    text\n    url\n    __typename\n  }\n  cardURL\n  description\n  imageURL {\n    light\n    dark\n    __typename\n  }\n  subtitle\n  title\n  uuid\n  __typename\n}\n"
}

  response = requests.post(api_url, cookies=cookies, headers=headers, json=json_data_v2)
  return response

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"operationName":"GetTrips","variables":{"cursor":"10","fromTime":1698818400000,"toTime":1701413999999},"query":"query GetTrips($cursor: String, $fromTime: Float, $toTime: Float) {\\n  getTrips(cursor: $cursor, fromTime: $fromTime, toTime: $toTime) {\\n    count\\n    pagingResult {\\n      hasMore\\n      nextCursor\\n      __typename\\n    }\\n    reservations {\\n      ...TripFragment\\n      __typename\\n    }\\n    trips {\\n      ...TripFragment\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment TripFragment on Trip {\\n  beginTripTime\\n  disableCanceling\\n  driver\\n  dropoffTime\\n  fare\\n  isRidepoolTrip\\n  isScheduledRide\\n  isSurgeTrip\\n  isUberReserve\\n  jobUUID\\n  marketplace\\n  paymentProfileUUID\\n  status\\n  uuid\\n  vehicleDisplayName\\n  waypoints\\n  __typename\\n}\\n"}'
#response = requests.post('https://riders.uber.com/graphql', cookies=cookies, headers=headers, data=data)

flag = False
ride_list = []
# get all trips (uuid)
while flag is False:
  response = get_rides(fromTime, toTime, cursor)
  print(response)
  json_response = response.json()
  print(json_response)
  rides = json_response["data"]["activities"]["past"]["activities"]
  if len(rides) < 1:
    break
  ride_list.extend([ride['uuid'] for ride in rides])
  cursor = str(int(cursor) + 10)
  flag = True

len(ride_list)



# Get individual RIDE
def get_ride(ride_id, api_url=api_url, cookies=cookies):


  headers = {
      'authority': 'riders.uber.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'sec-ch-prefers-color-scheme': 'light',
      'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'x-csrf-token': 'x',
  }

  json_data = {
      'operationName': 'GetTrip',
      'variables': {
          'tripUUID': ride_id,
      },
      'query': 'query GetTrip($tripUUID: String!) {\n  getTrip(tripUUID: $tripUUID) {\n    trip {\n      beginTripTime\n      cityID\n      countryID\n      disableCanceling\n      disableRating\n      driver\n      dropoffTime\n      fare\n      guest\n      isRidepoolTrip\n      isScheduledRide\n      isSurgeTrip\n      isUberReserve\n      jobUUID\n      marketplace\n      paymentProfileUUID\n      status\n      uuid\n      vehicleDisplayName\n      vehicleViewID\n      waypoints\n      __typename\n    }\n    mapURL\n    polandTaxiLicense\n    rating\n    receipt {\n      carYear\n      distance\n      distanceLabel\n      duration\n      vehicleType\n      __typename\n    }\n    __typename\n  }\n}\n',
  }

  response = requests.post(api_url, cookies=cookies, headers=headers, json=json_data)
  return response


ride_detail_list = []
for ride_id in ride_list:
  response = get_ride(ride_id)
  json_response = response.json() # beginTripTime, fare, waypoints
  ride = json_response["data"]["getTrip"]["trip"]
  # check for canceled rides > continue
  if ride['status'] == 'CANCELED':
    continue
  # TripTime format updated 10/2024: "10/8/2024, 9:36:05 PM" in local time
  ## reverted 11/1/2024
  ride_time_UTC = datetime.strptime(ride['beginTripTime'], '%a %b %d %Y %H:%M:%S %Z%z (Coordinated Universal Time)')
  #ride_time_UTC = datetime.strptime(ride['beginTripTime'], '%m/%d/%Y, %H:%M:%S %p')
  #ride_time = ride_time_UTC.astimezone(tz.gettz('US/Mountain')).strftime('[%A] %B %d, %Y')
  ride_time = ride_time_UTC.strftime('[%A] %B %d, %Y')
  ride_detail_list.append({'ride_id':ride_id,'ride_time':ride_time, 'ride_fare':ride['fare'], 'ride_from':ride['waypoints'][0], 'ride_to':ride['waypoints'][1]})

#print(ride_detail_list[2])

def get_ride_reciept(ride_id, api_url=api_url, cookies=cookies):
  headers = {
      'authority': 'riders.uber.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'sec-ch-prefers-color-scheme': 'dark',
      'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'x-csrf-token': 'x',
  }

  json_data = {
      'operationName': 'GetReceipt',
      'variables': {
          'tripUUID': ride_id,
          'timestamp': '',
      },
      'query': 'query GetReceipt($tripUUID: String!, $timestamp: String) {\n  getReceipt(tripUUID: $tripUUID, timestamp: $timestamp) {\n    actionList {\n      type\n      helpNodeUUID\n      __typename\n    }\n    receiptData\n    receiptsForJob {\n      timestamp\n      type\n      eventUUID\n      __typename\n    }\n    __typename\n  }\n}\n',
  }

  response = requests.post(api_url, cookies=cookies, headers=headers, json=json_data)
  return response

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"operationName":"GetReceipt","variables":{"tripUUID":"<redacted>","timestamp":""},"query":"query GetReceipt($tripUUID: String!, $timestamp: String) {\\n  getReceipt(tripUUID: $tripUUID, timestamp: $timestamp) {\\n    actionList {\\n      type\\n      helpNodeUUID\\n      __typename\\n    }\\n    receiptData\\n    receiptsForJob {\\n      timestamp\\n      type\\n      eventUUID\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}'
#response = requests.post('https://riders.uber.com/graphql', cookies=cookies, headers=headers, data=data)

## now get the reciept!!
for ride_detail in ride_detail_list:
  # Go to ride's reciept page
  response = get_ride_reciept(ride_detail['ride_id'])
  # capture reciept screen
  json_response = response.json()
  try:
    html = json_response['data']['getReceipt']['receiptData']
    # save to disk
    htmldoc = HTML(string=html, base_url='')
    htmldoc.write_pdf(f"{base_url}{ride_detail['ride_id']}.pdf")
    print(f"[+] Ride {ride_detail['ride_id']} receipt printed.")
  except:
    print(f"[-] Ride {ride_detail['ride_id']} failed to get receipt.")

# Export RIDES as Excel doc named as MonthYear
#file_name = datetime.fromtimestamp(fromTime / 1000).astimezone(tz.gettz('US/Mountain')).strftime('%B_%Y') + '.xlsx'
file_name = datetime.fromtimestamp(int(fromTime)/1000).strftime('%B_%Y') + '.xlsx'
print(file_name)

ride_df = pd.DataFrame(ride_detail_list)

try:
  ride_df.to_excel(base_url + file_name)
  print(f"[+] Ride details saved as {file_name}.")
except:
  print(f"[-] Ride details failed saving to file.")
