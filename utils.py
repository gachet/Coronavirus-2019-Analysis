import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
    sns.lineplot(df.index, df['Deaths']*100/df['Confirmed'])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.xticks(rotation=60)

def recovery_rate(df, title):
    sns.lineplot(df.index, df['Recovered']*100/df['Confirmed'])
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
    
    plt.ylabel(total_data.columns[0])

    for p in ax.patches:
        ax.annotate(p.get_height(), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', 
                    va = 'center', 
                    xytext = (0, 10), 
                    textcoords = 'offset points', 
                    fontsize=18)

def daily_cases(df, title):
    sns.lineplot(df.index, df['Confirmed'].diff())
    sns.lineplot(df.index, df['Deaths'].diff(), color='red')
    sns.lineplot(df.index, df['Recovered'].diff(), color='green')
    sns.lineplot(df.index, df['Active'].diff(), color='orange')
    
    plt.legend(['Confirmed', 'Deaths', 'Recovered', 'Active'])
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Cases')
    plt.xticks(rotation=60)