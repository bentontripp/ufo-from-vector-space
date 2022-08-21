import pandas as pd
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
    # replace 'nan' with np.nan
    durations = {
        k: val for k, val in zip(
            durations.keys(),
            list(map(lambda v: v if v != 'nan' else None, durations.values()))
        )
    }
    df["Updated_Duration"] = df.Duration.map(durations)
    return df


if __name__ == '__main__':
    date_start = '202107'
    date_end = '202206'
    df = cleanTable(file="src/data/UFOs{}-{}.csv".format(date_start, date_end))
    print(df.loc[df.Duration == 'Looking at the sky']\
        [['Timestamp', 'Posted', 'Duration', 'Updated_Duration']])
