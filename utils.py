import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime

def total_cases_pie(df, title):
    values = df.drop(['Confirmed'], axis=1)[-1:].values.transpose()
    plt.pie(values, 
            labels=['Deaths', 'Recovered', 'Active'], 
            colors=['red', 'green', 'orange'],
            autopct='%.2f%%', 
            startangle=90, 
            shadow=True)
    plt.title(title)

def total_cases_lineplot(df, title):
    sns.lineplot(df.index, df['Confirmed'])
    sns.lineplot(df.index, df['Deaths'], color='red')
    sns.lineplot(df.index, df['Recovered'], color='green')
    sns.lineplot(df.index, df['Active'], color='orange')
    plt.legend(['Confirmed', 'Deaths', 'Recovered', 'Active'])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Cases')
    plt.xticks(rotation=60)

def mortality_rate(df, title):
    sns.lineplot(df.index, df['Deaths']*100/df['Confirmed'], color='red')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.xticks(rotation=60)

def recovery_rate(df, title):
    sns.lineplot(df.index, df['Recovered']*100/df['Confirmed'], color='green')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.xticks(rotation=60)

def total_latest_barplot(df):
    dictByLastDate = {'Confirmed': df['Confirmed'].tolist()[-1], 
                      'Deaths': df['Deaths'].tolist()[-1], 
                      'Recovered': df['Recovered'].tolist()[-1], 
                      'Active': df['Active'].tolist()[-1]}

    total_column = 'Total cases by ' + max(df.index).strftime('%b %d, %Y')
    total_data = pd.DataFrame.from_dict(dictByLastDate, 
                                        orient='index', 
                                        columns=[total_column])
    
    x = total_data.index
    y = total_data[total_column]
    ax = sns.barplot(x,  y,  palette=['#1f77b4', 'red', 'green', 'orange'])

    for p in ax.patches:
        ax.annotate(int(p.get_height()), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', 
                    va = 'center', 
                    xytext = (0, 10), 
                    textcoords = 'offset points', 
                    fontsize=18)
    
    plt.ylabel(total_data.columns[0])

def daily_cases(df, title):
    date_column = pd.to_datetime(df.index).strftime('%b %d')
    
    fig, axs = plt.subplots(3, 1, sharex=True, squeeze=False, figsize=(20,12))
    
    sns.barplot(date_column, df['Confirmed'].diff(), color='#1f77b4', ax=axs[0][0])
    sns.barplot(date_column, df['Deaths'].diff(), color='red', ax=axs[1][0])
    sns.barplot(date_column, df['Recovered'].diff(), color='green', ax=axs[2][0])
    
    fig.suptitle(title)
    plt.xticks(rotation=90)

def total_cases_by_country(df, column, palcolor):
    y = df.index
    x = df[column]
    
    xvalues = x.tolist()
    maxvalue = max(xvalues)
    dflen = len(xvalues)
    
    rank = [int((maxvalue - val) * dflen/(maxvalue + 1)) for val in xvalues]
    palette = sns.color_palette(palcolor, dflen)
    
    ax = sns.barplot(x=x, y=y, orient='h', palette=np.array(palette)[rank])
    
    for p in ax.patches:
        ax.annotate(int(p.get_width()), 
                    (p.get_width(), p.get_y() + p.get_height() / 2.), 
                    ha = 'left', 
                    va = 'center', 
                    fontsize=18)
    
    plt.title('Total {} by Country'.format(column))

def countries_comparison(df_countries, column, title):
    for df in df_countries:
        df = df.groupby(['Observed']).sum()
        sns.lineplot(df.index, df[column])
    
    plt.legend([df['Country/Region'].iloc[0] for df in df_countries])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Cases')
    plt.xticks(rotation=60)
    
def total_cases_map(df, column, color_continuous, height=800, projection='equirectangular'):
    fig = px.scatter_geo(df, lat='Lat', lon='Long', height=height,
                         color=column, size=f'{column}_size', 
                         projection=projection, animation_frame='Date', 
                         title='{} Cases Over Time'.format(column), 
                         color_continuous_scale=color_continuous)
    fig.show()