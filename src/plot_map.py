from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt


# https://datascientyst.com/plot-latitude-longitude-pandas-dataframe-python/
def getMap(df, dissolvedus_path, mapsvg_path, mapjpg_path):
    if df.Coords.dtype == list:
        coords = df.Coords.apply(eval)
    else:
        coords = df.Coords
    geometry = [Point(c) for c in coords]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)
    # Load US_body from disc
    states = gpd.read_file(dissolvedus_path)
    gdf.plot(ax=states.plot(), marker='o', color='red', markersize=15)
    plt.axis('off')
    plt.gca().set_position([0,0,1,1])
    plt.savefig(mapsvg_path, format='svg', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.savefig(mapjpg_path, dpi=1200, bbox_inches='tight', pad_inches=0, transparent=True)
    return plt