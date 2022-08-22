import pandas as pd
import numpy as np
import re
import json


def cleanTable(file: str):
    """
    Clean dataframe of UFO sightings
    """
    # read data
    df = pd.read_csv(file)
    # filter columns; rename
    df = df.rename(columns={'Date / Time': 'Timestamp'})
    # filter to USA (excluding minor outlying islands)
    df = df.loc[df.Country == 'USA'].reset_index(
        drop=True).drop(columns='Country')
    # read json duration data
    with open('src/data/durations.json') as f:
        durations = json.loads(f.read())
        f.close()
    # map to `Updated_Duration`; replace 'nan' with np.nan
    df["Updated_Duration"] = df.Duration.map(durations).replace({'nan': np.nan})
    return df


if __name__ == '__main__':
    date_start = '202107'
    date_end = '202206'
    df = cleanTable(file="src/data/UFOs{}-{}.csv".format(date_start, date_end))
    print(df.loc[~df.Updated_Duration.isna()]\
        [['Timestamp', 'Posted', 'Duration', 'Updated_Duration']])
