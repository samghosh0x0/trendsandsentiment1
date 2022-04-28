import requests
import pandas as pd
from pandas import DataFrame
import sqlalchemy
import numpy as np
import datetime as dt
import os

##os.chdir("C:/Users/Administrator/AppData/Local/Programs/Python/Python35-32/test/Natural language/news/news_India/Collection")

bloombergquint = pd.read_csv('bloombergquint.csv', encoding = "ISO-8859-1")
business = pd.read_csv('business-standard.csv', encoding = "ISO-8859-1")
cnbc = pd.read_csv('cnbc.csv', encoding = "ISO-8859-1")
economictimes = pd.read_csv('economictimes.csv', encoding = "ISO-8859-1")
yahoo = pd.read_csv('finance_yahoo.csv', encoding = "ISO-8859-1")
financialexpress = pd.read_csv('financialexpress.csv', encoding = "ISO-8859-1")
livemint = pd.read_csv('livemint.csv', encoding = "ISO-8859-1")
moneycontrol = pd.read_csv('moneycontrol.csv', encoding = "ISO-8859-1")
ndtv = pd.read_csv('profit_ndtv.csv', encoding = "ISO-8859-1")
reuters = pd.read_csv('reuters.csv', encoding = "ISO-8859-1")

frames = [bloombergquint, business, cnbc, economictimes, yahoo, financialexpress,
          livemint, moneycontrol, ndtv, reuters]

all_news_ind = pd.concat(frames, ignore_index = True)
timelog = dt.datetime.now()
all_news_ind.insert(3,'Timelog',timelog, allow_duplicates=False)


##Connecting to MySQL
eng = sqlalchemy.create_engine("mysql+pymysql://root:xxx@localhost/xxx")

##User_stats_Gr_Indexed.to_csv('User_Stats_Grouped.csv')
if (len(all_news_ind)>0):
    print("in")
    all_news_ind.to_sql(name='news_indian_headlines', con=eng, if_exists = 'replace', index=True)
    #print(all_news_ind)
    all_news_ind.to_csv('all_newsind.csv', index= False)
##closing the MySQL connection
eng.dispose()




