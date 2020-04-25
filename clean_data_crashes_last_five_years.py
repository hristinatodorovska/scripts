import pandas as pd
import datetime
import sys
import fiona
import geopandas as gpd
import json
from shapely.geometry import Point, shape
from shapely.geometry.polygon import Polygon

pd.options.mode.chained_assignment = None # default='warn'


def coor_to_nbr(longit, lat, shape_file):
    """
    for each point with Longitude and Latitude return Suburb Name
    :param longit: longitude
    :param lat: Latitude
    :param shape_file:
    :return: Suburb
    """
    mypoint = Point(longit, lat)

    with fiona.open(shape_file) as shp:
        polygons = [poly for poly in shp]
    poly_idx = [i for i, poly in enumerate(polygons)
                if mypoint.within(shape(poly['geometry']))]

    if not poly_idx:
        return None
    else:
        # Take first polygon that overlaps since may overlap with several if on border
        match = polygons[poly_idx[0]]
        return match['properties']['VIC_LOCA_2']


def df_to_geojson(df):
    """
    Convert Dataframe df into geojson
    :param df: Dataframe
    :return: geojson
    """
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Point', 'coordinates': []}}
        feature['geometry']['coordinates'] = [row['longitude'], row['latitude']]
        feature['properties']['id'] = row['record_id']

        geojson['features'].append(feature)

    return geojson


sys.stdout.write("-------------START-------------\n")
# columns that will bes used
fields = ["X", "Y", "OBJECTID", "ACCIDENT_DATE", "ACCIDENT_TIME", "ALCOHOLTIME", "ACCIDENT_TYPE", "DAY_OF_WEEK",
          "DCA_CODE", "LIGHT_CONDITION", "LONGITUDE", "LATITUDE", "LGA_NAME", "REGION_NAME", "TOTAL_PERSONS",
          "INJ_OR_FATAL",
          "FATALITY", "SERIOUSINJURY", "OTHERINJURY", "NONINJURED", "MALES", "FEMALES", "BICYCLIST", "PASSENGER",
          "DRIVER",
          "PEDESTRIAN", "PILLION", "MOTORIST", "UNKNOWN", "PED_CYCLIST_5_12", "PED_CYCLIST_13_18", "OLD_PEDESTRIAN",
          "OLD_DRIVER",
          "YOUNG_DRIVER", "ALCOHOL_RELATED", "UNLICENCSED", "NO_OF_VEHICLES", "HEAVYVEHICLE", "PASSENGERVEHICLE",
          "MOTORCYCLE",
          "PUBLICVEHICLE", "DEG_URBAN_NAME", "DEG_URBAN_ALL", "LGA_NAME_ALL", "REGION_NAME_ALL"]

sys.stdout.write("Read the file Crashes_Last_Five_Years.csv \n")


# Read the data
data = pd.read_csv("./import_data/Crashes_Last_Five_Years.csv", usecols=fields)

# Read the Ploygon for Victoria
shpFile = './vic_suburb_boundary/VIC_LOCALITY_POLYGON_shp.shp'
vic = gpd.read_file(shpFile)

sys.stdout.write("Filter Data \n")

# filter only the accident with BICYCLIST
bikeData = data.loc[data['BICYCLIST'] != 0, ]

# separate Year and Month in different column
bikeData.loc[:, 'Year'] = bikeData["ACCIDENT_DATE"].apply(lambda row: row.split("/")[2])
bikeData.loc[:, 'Month'] = bikeData["ACCIDENT_DATE"].apply(lambda row: row.split("/")[1])
bikeData.loc[:, 'Month_name'] = bikeData["Month"].apply(lambda row: datetime.date(1900, int(row), 1).strftime('%B'))

# reset the index
bikeData.reset_index(drop=True, inplace=True)
sys.stdout.write("Find Suburb \n")
# Find suburb based on Latitude Longitude of the accident
bikeData.loc[:, 'Suburb'] = bikeData.apply(lambda row: coor_to_nbr(row['LONGITUDE'], row['LATITUDE'], shpFile), axis=1)

# save clean data into csv file
bikeData.to_csv('./export_data/bike_crashes_last_five_years.csv', index=False)
sys.stdout.write("Save Filtered Data as bike_crashes_last_five_years.csv \n")

data = bikeData.loc[:, ["OBJECTID", "LONGITUDE", "LATITUDE", "Suburb"]].copy()
data.rename(columns={"OBJECTID": "record_id", "LONGITUDE": "longitude", "LATITUDE": "latitude", "Suburb" : "suburb"}, inplace=True)

# save regular JSON
data.to_json(r'./export_data/bike_crashes.json', orient='records')
sys.stdout.write("Save json file for Bike Crashes to bike_crashes.json   \n")

# convert to geojson format
geoJsonDf = df_to_geojson(data)

out_file = open("./export_data/accident_data.json", "w")
sys.stdout.write("Save geojson file for Bike Crashes to accident_data.json   \n")
json.dump(geoJsonDf, out_file)
out_file.close()

sys.stdout.write("-------------FINISH-------------")
