# -*- coding: utf-8 -*-

import streamlit as st

@st.cache_data
def get_data(sorce):
    """
    Parameters
    ----------
    source: TYPE
        DESCRIPTION.

    Returns
    -------
    data: TYPE
        DESCRIPTION.

    """
    import functions as f
    import requests
    import pandas as pd

    if "http://www" in sorce:
        response = requests.get(sorce)
        content = response.content
        df = pd.read_excel(content, skiprows=12, sheet_name=None)
    else:
        df = pd.read_excel(sorce, skiprows=12, sheet_name=None)

    data = pd.DataFrame()
    for key, value in df.items():
        value = value.drop(value.columns[1], axis=1)
        value.insert(0, "מגזר", key)
        data = pd.concat([data, value], axis=0)

    data = data.set_index(["מגזר", "שם פרטי"]).stack().reset_index()
    data.columns = ["מגזר", "שם", "שנה", "נולדו"]
    data.replace(["..", "."], [0, 0], inplace=True)
    return data

@st.cache_data
def data_identifiers(data):
    """
    summerise the data identifiers

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.

    Returns
    -------
    gender : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    year : TYPE
        DESCRIPTION.

    """
    import pandas as pd
    gender = data["מגזר"].unique().tolist()
    name = data["שם"].unique().tolist()
    year = data["שנה"].unique().tolist()
    return gender, name, year



def max_born_at_year(name, data):
    """
    Find the year most of a name was born.
    Parameters
    ----------
    name : str
        a name.
    data : DataFrame

    Returns
    -------
    max_born : int
        max babys that boarn.
    max_born_year : int
        the max year that babys was born with the name.

    """
    import pandas as pd
    mxborn = data.groupby(["שם", "שנה"])["נולדו"].sum().loc[name]
    max_born = mxborn.max()
    max_born_year = mxborn.idxmax()
    return max_born, max_born_year


def first_year_born(data, name):
    '''
    Find first year name exist

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.

    Returns
    -------
    first_year : TYPE
        DESCRIPTION.

    '''
    import pandas as pd
    firstborn = data.groupby(["שם", "שנה"])["נולדו"].sum().loc[name]
    for year, born in firstborn.items():
        if born > 0:
            first_year = year
            break
        return first_year


def present_name_in_year(data, name, year):
    """
    Find % of the name from a year total borns

    Parameters
    ----------
    data : TYPE
        DESCRIPTION.
    name : TYPE
        DESCRIPTION.
    year : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    total_name_data = data.groupby(["שם"])["נולדו"].sum()
    total_prs_name = (total_name_data.loc[name]/total_name_data.sum())*100
    return round(total_prs_name, 2)

def name_description(name):
    import requests
    from bs4 import BeautifulSoup
    try:
        url = f"https://www.itim.org.il/name-archive/{name}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        name_description = soup.find(
            'div', class_='names-results__description').text
    except:
        name_description = "מצטערים, אין שם כזה במאגר"
    return name_description

def summary_name_year(data):
    """
    summary name and year

    Parametees
    ----------
    data : df
        DESCRIPTION.

    Returns
    -------
    df : df
        DESCRIPTION.

    """
    df=data.groupby(["שם", "שנה"])["נולדו"].sum()
    return df


