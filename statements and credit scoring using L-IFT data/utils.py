import pandas as pd
import datetime as dt

def filter_by_year(df:pd.DataFrame, date_col: str, year:int) -> pd.DataFrame:
    return df[(df[date_col] >= dt.date(year, 1, 1)) & (df[date_col] <=dt.date(year, 12, 31))].reset_index().drop(columns='index')


def filter_by_year_month(df:pd.DataFrame, date_col: str, year:int, month:int):
    p = pd.Period(f'{year}-{month}-1')
    days = p.daysinmonth
    return df[(df[date_col] >= dt.date(year, month, 1)) & (df[date_col] <=dt.date(year, month, days))].reset_index().drop(columns='index')


def filter_up_to(df: pd.DataFrame, date_col: str, year: int, month: int=None):
    if month == None:
        month = 12
    p = pd.Period(f'{year}-{month}-1')
    days = p.days_in_month
    return df[df[date_col] <= dt.date(year, month, days)]


def get_unique_years(df: pd.DataFrame, date_col: str):
    not_na = df[~df[date_col].isna()]
    return not_na[date_col].apply(lambda x: x.year).unique()


def get_unique_months(df: pd.DataFrame, date_col: str):
    not_na = df[~df[date_col].isna()]
    return not_na[date_col].apply(lambda x: x.month).unique()
    

def get_lastest_month(df: pd.DataFrame, date_col:str, year:int):
    filtered = filter_by_year(df, date_col, year)
    return filtered[date_col].apply(lambda x: x.month).max()


def get_latest_year(df:pd.DataFrame, date_col:str):
    date_ordered = df[~df[date_col].isna()][date_col].sort_values().reset_index().drop(columns='index')
    return date_ordered.loc[len(date_ordered)-1][0].year

def get_years_list(df: pd.DataFrame, date_col:str):
    years = get_unique_years(df, date_col)
    return sorted(list(years[years >= 2021]))

def get_months_list(df: pd.DataFrame, year:float, date_col:str):
    df2 = filter_by_year(df, date_col, year)
    return sorted(list(get_unique_months(df2, date_col)))


