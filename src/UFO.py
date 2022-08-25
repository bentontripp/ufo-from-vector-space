import sys
sys.path.insert(0,'src')
from config import Config
from clean_data import cleanTable, getFeatures
from get_data import getTable
from plot_map import getMap
import os
import pandas as pd

CONFIG = Config()

class US_UFO_data:

    def __init__(self):
        raw_path = CONFIG.Data['raw']
        processed_path = CONFIG.Data['processed']
        final_path = CONFIG.Data['final']
        if os.path.exists(processed_path):
            self.data = pd.read_csv(processed_path)
        elif not os.path.exists(processed_path) and os.path.exists(raw_path):
            self.data = cleanTable(
                file=raw_path, 
                durations_path=CONFIG.Data['durations'],
                locations_path=CONFIG.Data['locations'],
                dissolvedus_path=CONFIG.Data['dissolvedus']
                )
            self.data.to_csv(processed_path, index=False)
        else:
            getTable(raw_path=raw_path)
            self.data = cleanTable(
                file=raw_path, 
                durations_path=CONFIG.Data['durations'],
                locations_path=CONFIG.Data['locations'],
                dissolvedus_path=CONFIG.Data['dissolvedus']
                )
            self.data.to_csv(processed_path, index=False)
        if os.path.exists(final_path):
            self.features = getFeatures(self.data)
            self.features.to_csv(final_path)
            self.features = pd.read_csv(final_path, index_col="Timestamp")
        else:
            self.features = getFeatures(self.data)
            self.features.to_csv(final_path)
        self.map = getMap(
            self.data, 
            inlandstates_path=CONFIG.Data['inlandstates'], 
            mapsvg_path=CONFIG.Plots['mapsvg']
            )

if __name__ == '__main__':
    ufo = US_UFO_data()
    print(ufo.data.head())
    print(ufo.features.head())