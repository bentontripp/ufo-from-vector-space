from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt

# https://datascientyst.com/plot-latitude-longitude-pandas-dataframe-python/
def get_map(df):
    geometry = [Point(c) for c in df.Coords]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    # Load US_body from disc
    states = gpd.read_file('src/data/state.shp')
    gdf.plot(ax=states.plot(figsize=(15,15)), marker='o', color='red', markersize=15)
    return plt