# Python scripts for cleaning and converting the data

## Libraries Required


```bash
pandas
fiona
geopandas
gpxpy
```
### 1. Cleaning Accident data and converting into geojson
```
clean_data_crashes_last_five_years.py
```
exported data saved into:
```
export_data\bike_crashes_last_five_years.csv - CSV
export_data\bike_crashes.json - JSON
export_data\accident_data.json - GEOJSON

```
### 2.  Vic Road Bike Path
```
vic_road_to_geojson.py
```
exported data saved into:
```
export_data\Trails.json - GEOJSON

```

### 3. Key Bike Transport Routes
```
zone_bike_path.py
```
exported data saved into:
```
export_data\red_trail.json - GEOJSON
export_data\orang_trail.json - GEOJSON
export_data\other_trail.json - GEOJSON

```

### 4. Beginner Off Road Trails
```
off_road_beginner.py
```
exported data saved into:
```
export_data\beginner.json - GEOJSON

```
### 5. Intermediate Off Road Trails
```
off_road_intermediate.py
```
exported data saved into:
```
export_data\intermediate.json - GEOJSON

```
### 6. Intermediate Off Road Trails
```
off_road_advanced.py
```
exported data saved into:
```
export_data\advanced.json - GEOJSON

```