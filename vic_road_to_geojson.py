import pandas as pd
import sys
import geopandas as gpd
import json


def coord_lister(geom):
    """
    Return coords from geometry
    :param geom:
    :return:
    """
    coords = list(geom.coords)
    return coords


def type_lister(geom):
    """
    Return geometry type
    :param geom:
    :return:
    """
    type = geom.type
    return type


def df_to_geojson(df):
    """
    Convert Dataframe df into geojson
    :param df: Dataframe
    :return: geojson
    """
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type': 'Feature', 'properties': {},
                   'geometry': {'type': row['type'], 'coordinates': row['coordinates']}}

        geojson['features'].append(feature)

    return geojson


sys.stdout.write("-------------START-------------\n")

sys.stdout.write("Load bike trials (Shape file)  \n")
# Read the Bike Lines shp file
shpFile = './vic_road/TR_ROAD.shp'
road = gpd.read_file(shpFile)

sys.stdout.write("Filter Data \n")
bike_road = road[road['CLASS_CODE'] == 12]
bike_road.reset_index(drop=True, inplace=True)

geoDf = pd.DataFrame(columns=['type', 'coordinates'])

geoDf['type'] = bike_road['geometry'].apply(type_lister)
geoDf['coordinates'] = bike_road['geometry'].apply(coord_lister)

geoJsonDf = df_to_geojson(geoDf)

out_file = open("./export_data/Trails.json", "w")
json.dump(geoJsonDf, out_file, indent=1)
out_file.close()
sys.stdout.write("Save geojson file for vic road bike path to Trails.json   \n")

sys.stdout.write("-------------FINISH-------------\n")
