import pandas as pd
import json, re, certifi, urllib3
from bs4 import BeautifulSoup

def getDateStrings(
    date_start:str,
    date_end:str
    ):
    """
    Get date range between `date_start` and `date_end` (inclusive); dates formatted as `yyyymm`
    """
    start_year = int(date_start[:-2])
    start_month = int(date_start[-2:])
    end_year = int(date_end[:-2])
    end_month = int(date_end[-2:])
    if start_year < end_year:
        dates = [str(start_year) + str(month).zfill(2) for month in range(start_month, 13)]
        if end_year - start_year > 1:
            for i in range(1, end_year - start_year):
                dates += [str(i) + str(month).zfill(2) for month in range(1, 13)]
        dates += [str(end_year) + str(month).zfill(2) for month in range(1, end_month + 1)]
    else:
        dates = [str(start_year) + str(month).zfill(2) for month in range(start_month, end_month + 1)]
    return dates

def cleanTable(df:pd.DataFrame):
    """
    Clean dataframe of UFO sightings
    """
    pass

def getTable(
    date_start:str, 
    date_end:str
    ):
    """
    Get UFO data in the USA between `date_start` and `date_end` (inclusive); dates formatted as 'yyyymm'
    """
    dates = getDateStrings(date_start, date_end)
    tbls = list()
    http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
    for date_str in dates:
        base_url = "https://nuforc.org/webreports/ndxe"
        r = http.request('GET', base_url + date_str + ".html")
        html = r.data
        bs = BeautifulSoup(html, features="lxml")
        tbls.append(pd.read_html(str(bs.find_all("table")))[0])
    # concatenate dataframes
    df = pd.concat(tbls)
    # filter columns; rename 
    df = df[['Date / Time', 'State', 'Country', 'Shape', 'Duration']]\
        .rename(columns={'Date / Time':'Timestamp'})
    # filter to USA (excluding minor outlying islands)
    df = df.loc[df.Country == 'USA'].reset_index(drop=True).drop(columns='Country')
    return df

if __name__ == '__main__':
    start = '202107'
    end = '202206'
    df = getTable(start, end)
    print(df)
    print(df.Shape.unique())
    print(len(df.Duration.unique()))