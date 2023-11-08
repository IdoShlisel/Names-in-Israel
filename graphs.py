# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 00:31:44 2023

@author: idosh
"""

def name_by_year(data,names,show=False):
    '''
    Generating graph of a born vs year

    Parameters
    ----------
    data : dataframe
        main dataframe.
    names : list
        list of names.
    show : bool, optional
        if Show is True graph is show for dev . The default is False.

    Returns
    -------
    fig : Plotly go object
        fig object.

    '''
    import plotly.express as px
    from plotly.offline import plot
    #changing the df
    df=data.groupby(["שם", "שנה"])["נולדו"].sum()
    names_df=df[names].reset_index()
    
    fig = px.line(names_df, x="שנה", y="נולדו",color="שם",template='plotly_white',markers="0")
    
    if show==True:
        plot(fig)
        
    return fig


def treemap_names(data,year,N_names,sector=True,show=False):
    """
    produce a treemap of the names that born in a selected year.

    Parameters
    ----------
    data : dataframe
    year : int.
        selected year.
    N_names : int
        how many names to show.
    sector : bool, optional
        If True- show a treemap with sector seperation. The default is True.
    show : TYPE, optional
        show graph. The default is False.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    import plotly.express as px
    from plotly.offline import plot
    import pandas as pd
    df=data[data['שנה']==year]
    df_no_sector=pd.DataFrame()
    if sector==True:
        df_sort=df.sort_values(["מגזר","נולדו"],ascending=False).groupby('מגזר').head(N_names)     
        fig = px.treemap(df_sort,path=["מגזר",'שם'], values='נולדו',
                      template='plotly_white'
                          )
        if show==True:          
            plot(fig)
    else:
        df_no_sector=df.groupby('שם').sum().reset_index().sort_values(["נולדו"],ascending=False).head(N_names).reset_index().drop(columns=["index"])  
        fig = px.treemap(df_no_sector,path=["שם"],values="נולדו",template='plotly_white')
        fig.data[0].textinfo='label+text+value'
        if show==True:          
            plot(fig)
        
    return  fig


def pichart_name_by_sector(data,name, show=False):
    """
    pi chart show the name distribution by sector in all history

    Parameters
    ----------
    data : df
        dataframe .
    name : str
        the sekected name.
    show : bool, optional
        show graph. The default is False.

    Returns
    -------
    fig : TYPE
        DESCRIPTION.

    """
    df=data[data["שם"]==name].groupby("מגזר").sum().reset_index()
    import plotly.express as px
    from plotly.offline import plot
    fig = px.pie(df, values='נולדו', names='מגזר', color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    if show==True:
        plot(fig)
    
    return fig



