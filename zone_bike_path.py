import pandas as pd
import json
import sys


def df_to_geojson(df, red, orange):
    """
    Convert Dataframe df into geojson and create three geojson based on the property name
    :param df: Data Frame
    :param red: array
    :param orange: array
    :return: array with three geojson elements [RED, ORANGEE, OTHER]
    """
    red_geojson = {'type': 'FeatureCollection', 'features': []}
    orange_geojson = {'type': 'FeatureCollection', 'features': []}
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type': row['type'], 'properties': row['properties'], 'geometry': row['geometry']}
        if row['properties']['Name'] in red:
            red_geojson['features'].append(feature)
        elif row['properties']['Name'] in orange:
            orange_geojson['features'].append(feature)
        else:
            geojson['features'].append(feature)

    return [red_geojson, orange_geojson, geojson]


sys.stdout.write("-------------START-------------\n")

# Read the data
data = json.load(open("./import_data/Key_Bike_Transport_Routes.geojson"))
df = pd.DataFrame(data["features"])

red = ['Johnson St & Studley Park Rd', 'Church St & Chapel St',
       'Sydney Rd', 'Elizabeth St', 'Collins St', 'Clarendon St',
       'Spencer St', 'Lonsdale Connector', 'Hopetoun Bridge',
       'Blackshaws Rd to Clelland Rd (Kororoit link)', 'Smith St' ]


orange = ['Gertrude St & Langridge St', 'High St', 'St Kilda Rd & Nepean Hwy',
          'Flemington Rd', 'Exhibition St',
          'Sages Rd to Metropolitan Ring Rd via Hume Hwy', 'Grattan St']

df_zones = df_to_geojson(df, red, orange)

red_file = open("./export_data/red_trail.json", "w")
json.dump(df_zones[0], red_file, indent=1)
red_file.close()
sys.stdout.write("Save RED trail\n")

orange_file = open("./export_data/orange_trail.json", "w")
json.dump(df_zones[1], orange_file, indent=1)
orange_file.close()
sys.stdout.write("Save ORABGE trail\n")

other_file = open("./export_data/other_trail.json", "w")
json.dump(df_zones[2], other_file, indent=1)
other_file.close()
sys.stdout.write("Save OTHER trail\n")

sys.stdout.write("-------------FINISH-------------\n")
