import pandas as pd
import requests, re
from bs4 import BeautifulSoup

def getDateStrings(
    date_start -> str,
    date_end -> str
    ):
    """
    Get date range between `date_start` and `date_end` (inclusive); dates formatted as `yyyymm`
    """
    start_year = int(date_start[:-2])
    start_month = int(date_start[-2:])
    end_year = int(date_end[:-2])
    end_month = int(date_end[-2:])
    dates = [str(year) + str(month).zfill(2) for]
    pass

def combineTables(
    tbls -> list
    ):
    """
    Clean/Combine list of UFO tables (each from a date page)
    """
    pass

def getTable(
    date_start -> str, 
    date_end -> str
    ):
    """
    Get UFO data in the USA between `date_start` and `date_end` (inclusive); dates formatted as 'yyyymm'
    """
    dates = getDateStrings(date_start, date_end)
    tbls = list()
    for date_str in dates:
        base_url = "https://nuforc.org/webreports/ndxe"
        html = requests.get(base_url + date_str, verify=False).text
        bs = BeautifulSoup(html)
        tbls += bs.findAll("table")
    tbl = combineTables(tbls)
    return tbl

if __name__ == '__main__':
    start = '202107'
    end = '202206'
    data = getTable(start, end)