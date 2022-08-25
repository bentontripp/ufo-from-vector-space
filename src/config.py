import configparser
import os

def genConfig():
    # CREATE OBJECT
    config = configparser.ConfigParser()

    config['DEFAULT'] = {}

    # ADD SECTION
    config.add_section("DataPaths")
    config.add_section("PlotPath")
    # ADD SETTINGS TO SECTIONS
    config.set("DataPaths", "Final", "data/final/final.csv")
    config.set("DataPaths", "Processed", "data/processed/us_ufo_data.csv")
    config.set("DataPaths", "Raw", "data/raw/raw_us_data.csv")
    config.set("DataPaths", "Durations", "data/processed/durations.json")
    config.set("DataPaths", "Locations", "data/processed/locations.csv")
    config.set("DataPaths", "DissolvedUS", "data/maps/dissolved_us/dissolved_us_body.shp")
    config.set("DataPaths", "InlandStates", "data/maps/inland_states/inland_states.shp")
    config.set("PlotPath", "MapSVG", "docs/map.svg")


    # SAVE CONFIG FILE
    with open(r"config/configurations.ini", 'w') as configfileObj:
        config.write(configfileObj)
        configfileObj.flush()
        configfileObj.close()

    print("Config file 'configurations.ini' created")

    # PRINT FILE CONTENT
    read_file = open("config/configurations.ini", "r")
    content = read_file.read()
    print("Content of the config file are:\n")
    print(content)
    read_file.flush()
    read_file.close()

class Config:
    def __init__(self, gen=False):
        if gen is True or not os.path.exists('config/configurations.ini'):
            genConfig()
        # Config
        config = configparser.ConfigParser()
        config.read('config/configurations.ini')
        self.keys = config.keys()
        self.sections = config.sections()
        self.Data = config["DataPaths"]
        self.Plots = config["PlotPath"]
