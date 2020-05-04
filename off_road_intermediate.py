import pandas as pd
import json
import gpxpy
import glob
import sys


# use your path
path = r'./import_data/blue/'
all_files = glob.glob(path + "/*.gpx")


def gpx_to_geojson(files):
    """
    Combining the data from all files in one geojson
    :param files: list of files name
    :return: geojson
    """
    geojson = {'type': 'FeatureCollection', 'features': []}
    coordinates = []
    for filename in files:
        gpx_file = open(filename, 'r')
        gpx_trial = gpxpy.parse(gpx_file)

        name = gpx_trial.tracks[0].name
        trial = gpx_trial.tracks[0].segments[0].points

        df = pd.DataFrame()
        for point in trial:
            df = df.append({'lon': point.longitude, 'lat': point.latitude, 'alt': point.elevation, 'time': point.time},
                           ignore_index=True)

        middle = int(df.shape[0] / 2)
        for index, row in df.iterrows():
            coordinates.append([row["lon"], row["lat"]])

        feature = {'type': 'Feature',
                   'properties': {'name': name, 'location': [df.loc[middle, 'lon'], df.loc[middle, 'lat']]},
                   'geometry': {'type': 'LineString', 'coordinates': coordinates}}
        geojson['features'].append(feature)

        return geojson


sys.stdout.write("Start formatting data \n")
offRoadIntermediate = gpx_to_geojson(all_files)

out_file = open("./export_data/Trails.json", "w")
intermediate = open("./export_data/intermediate.json", "w")
json.dump(offRoadIntermediate, intermediate, indent=1)
intermediate.close()
sys.stdout.write("Save intermediate trails\n")

