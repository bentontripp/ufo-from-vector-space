import sys
sys.path.insert(0,'src')
from clean_data import cleanTable, getFeatures
from get_data import getTable
from plot_map import getMap
import hydra
from omegaconf import DictConfig
from hydra.utils import to_absolute_path as abspath
import os
import pandas as pd

class US_UFO_data:

    @hydra.main(config_path="config", config_name='main')
    def __init__(self, config: DictConfig):
        raw_path = abspath(config.raw.path)
        processed_path = abspath(config.processed.path)
        final_path = abspath(config.final.path)
        print(raw_path, processed_path, final_path)
        if os.path.exists(processed_path):
            self.data = pd.read_csv(processed_path)
        elif not os.path.exists(processed_path) and os.path.exists(raw_path):
            self.data = cleanTable(raw_path)
            self.data.to_csv(processed_path, index=False)
        else:
            raw = getTable()
            raw.to_csv(raw_path, index=False)
            self.data = cleanTable(raw_path)
            self.data.to_csv(processed_path, index=False)
        if os.path.exists(final_path):
            self.features = getFeatures(self.data)
            self.features.to_csv(final_path)
            self.features = pd.read_csv(final_path, index_col="Timestamp")
        else:
            self.features = getFeatures(self.data)
            self.features.to_csv(final_path)
        self.map = getMap(self.data)

def main():
    ufo = US_UFO_data()

if __name__ == '__main__':
    main