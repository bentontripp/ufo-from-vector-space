from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt


# https://datascientyst.com/plot-latitude-longitude-pandas-dataframe-python/
def getMap(df, inlandstates_path, mapsvg_path):
    if df.Coords.dtype == list:
        coords = df.Coords.apply(eval)
    else:
        coords = df.Coords
    geometry = [Point(c) for c in coords]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    # Load US_body from disc
    states = gpd.read_file(inlandstates_path)
    gdf.plot(ax=states.plot(figsize=(15,15)), marker='o', color='red', markersize=15)
    plt.gca().set_position([0,0,1,1])
    plt.savefig(mapsvg_path)
    return plt