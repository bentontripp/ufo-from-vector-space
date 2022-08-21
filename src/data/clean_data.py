import pandas as pd
import re, json


def cleanTable(file:str):
    """
    Clean dataframe of UFO sightings
    """
    # read data
    df = pd.read_csv(file)
    # filter columns; rename 
    df = df.rename(columns={'Date / Time':'Timestamp'})
    # filter to USA (excluding minor outlying islands)
    df = df.loc[df.Country == 'USA'].reset_index(drop=True).drop(columns='Country')
    # TODO: read json duration data
    return df

if __name__ == '__main__':
    date_start='202107'
    date_end='202206'
    df = cleanTable(file="src/data/UFOs{}-{}.csv".format(date_start, date_end))
    print(df)