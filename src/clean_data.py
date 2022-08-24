import pandas as pd
import numpy as np
import json
import os
import geocoder 
import fiona
from shapely.geometry import shape
import numpy as np
from inpoly import inpoly2


# https://www.bingmapsportal.com; https://geocoder.readthedocs.io/providers/Bing.html
global BING_MAPS_KEY
BING_MAPS_KEY = os.environ.get('BING_MAPS')

def getLatLon(location):
    try:
        g = geocoder.bing(location, key=BING_MAPS_KEY)
        results = g.json
        return (results['lng'], results['lat'])
    except Exception as e:
        print('Error: {}'.format(e))
        return 'Location Not Found'

def evalCoord(coord):
    return eval(coord)


def toMinutes(t):
    tl = t.split(' ')
    unit = tl[-1]
    try:
        if unit == 'minutes':
            return float(tl[0])
        elif unit == 'seconds':
            return float(tl[0]) / 60
        elif unit == 'hours':
            return float(tl[0]) * 60
    except:
        print(tl)
        return t

def cleanTable(file):
    """
    Clean dataframe of UFO sightings
    """
    # read data
    df = pd.read_csv(
        file, 
        parse_dates=['Date / Time', 'Posted'],
        dtype={
            'Country':str, 
            'State':str, 
            'City':str,
            'Shape':str, 
            'Duration':str,
            'Summary':str,
            'Images':str
            })
    # filter columns; rename
    df = df.rename(columns={'Date / Time': 'Timestamp'})
    # filter to USA (excluding minor outlying islands)
    df = df.loc[df.Country == 'USA'].reset_index(
        drop=True).drop(columns='Country')
    # read json duration data
    with open('src/data/processed/durations.json') as f:
        durations = json.loads(f.read())
        f.close()
    # map to `Updated_Duration`; impute null with median
    df["Updated_Duration"] = df.Duration.map(durations).replace({'nan': np.nan})
    df.loc[~df.Updated_Duration.isna(), 'Updated_Duration'] = df.loc[~df.Updated_Duration.isna()].Updated_Duration.apply(toMinutes)
    df.loc[df.Updated_Duration.isna(), 'Updated_Duration'] = np.median(df.Updated_Duration.values)
    # get lat lon
    if os.path.exists('src/data/processed/locations.csv'):
        locations = pd.read_csv('src/data/processed/locations.csv')
        df['Coords'] = locations.Coords.apply(evalCoord)
        pass
    else:
        df['Coords'] = (df.City + ', ' + df.State).apply(getLatLon)
        df[['City', 'State', 'Coords']].to_csv('src/data/processed/locations.csv', index=False)
    # Lat/Lng columns
    df['Lat'] = df.Coords.apply(lambda c: c[0])
    df['Lng'] = df.Coords.apply(lambda c: c[1])
    # Filter to main body of US
    # https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
    geom = shape(fiona.open('src/data/maps/dissolved_us/dissolved_us_body.shp')[0]['geometry'])
    bounds = np.array([
        [geom.bounds[0], geom.bounds[3]], 
        [geom.bounds[0], geom.bounds[1]], 
        [geom.bounds[2], geom.bounds[1]], 
        [geom.bounds[2], geom.bounds[3]],
        [geom.bounds[0], geom.bounds[3]]
        ])
    coords = np.array(df.Coords.values.tolist())
    isin, ison = inpoly2(coords, bounds)
    df = df.loc[(isin | ison) & (df.State != 'ON')].reset_index(drop=True)
    # Images to Binary
    df.loc[~df.Images.isna(), 'Images'] = 1
    df.loc[df.Images.isna(), 'Images'] = 0
    # Clean Shape
    df.loc[df.Shape.isna() | df.Shape.isin(['Other', 'Unknown', 'Changing']), 'Shape'] = 'Other'
    return df

# Get features as numeric data
def getFeatures(df):
    shapes = list(df.Shape.unique())
    df = df.copy()
    df[shapes] = pd.get_dummies(df.Shape)
    df = df[['Timestamp', 'Lat', 'Lng', 'Updated_Duration', 'Images'] + shapes]
    df = df.set_index('Timestamp')
    return df