#Sources:
#1. https://medium.com/@lovespreadsheets/how-to-geocode-addresses-in-spreadsheets-using-python-780510615061
#2. https://developers.arcgis.com/labs/python/search-for-an-address/

import pandas as pd

from arcgis.gis import GIS
from arcgis.geocoding import geocode

from datetime import datetime

#directory storing data files
directory = 'data'

##############################################################################
#Geocoding addresses of all transplant centers
#and creating a directory of center code to coordinates
##############################################################################
transplant_df = pd.read_csv("./{}/transplantCenterData.csv".format(directory))

Address = []

centers = transplant_df["Transplant Center"].values.tolist()
cities = transplant_df["City"].values.tolist()

for i in range(len(centers)):
    Address.append(centers[i] + ", " + cities[i] + ", USA")

transplant_df["Address"] = Address

gis = GIS()

Lat = []
Long = []

for address in Address:
    geocode_result = geocode(address=address)
    latitude = str(geocode_result[0]['location']['y'])
    longitude = str(geocode_result[0]['location']['x'])
    Lat.append(latitude)
    Long.append(longitude)

transplant_df["Lat"] = Lat
transplant_df["Long"] = Long

transplant_df.to_csv("./{}/transplantCenterData.csv".format(directory), index=False)

##############################################################################
#Geocoding addresses of all OPO Centers
##############################################################################
OPO_df = pd.read_csv("./{}/OPODirectory.csv".format(directory))

Address = []

OPOs = OPO_df["Name "].values.tolist()
cities = OPO_df["Location "].values.tolist()

for i in range(len(OPOs)):
    Address.append(OPOs[i] + ", " + cities[i] + ", USA")

OPO_df["Address"] = Address

Lat = []
Long = []

for address in Address:
    geocode_result = geocode(address=address)
    latitude = str(geocode_result[0]['location']['y'])
    longitude = str(geocode_result[0]['location']['x'])
    Lat.append(latitude)
    Long.append(longitude)

OPO_df["Lat"] = Lat
OPO_df["Long"] = Long

OPO_df.to_csv("./{}/OPODirectory.csv".format(directory), index=False)
