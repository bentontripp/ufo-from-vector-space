import sys
sys.path.insert(0,'src')
from clean_data import cleanTable, getFeatures
from plot_map import get_map

class US_UFO_data:

    def __init__(self, date_start="202107", date_end="202206"):
        file="src/data/raw/UFOs{}-{}.csv".format(date_start, date_end)
        self.data = cleanTable(file)
        self.features = getFeatures(self.data)
        self.map = get_map(self.data)