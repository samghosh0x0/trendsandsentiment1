from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import numpy as np
import os
url = "http://www.bloombergquint.com"

r = requests.get(url)

soup = BeautifulSoup(r.content,  "html.parser")

headline_links = lambda tag: (getattr(tag, 'name', None) == 'a' and
                           'data-label' in tag.attrs)
results = soup.find_all(headline_links)
try :
    
    s=pd.DataFrame(results, index=None)
    s.columns = ['link']
    s.link = s['link'].apply(str)
    s['link'] = s['link'].map(lambda x: x.lstrip('<a data-label='))
    s.insert(0,'source',"http://www.bloombergquint.com", allow_duplicates=False)
    s['title'] =s['link'].str.extract('\"(.*?)\"\s',  expand=True)
    s['href'] =s['link'].str.extract('.*\"(.*)\".*',  expand=True)
    print(s)
    s['click'] = s[['source', 'href']].apply(lambda x: ''.join(x), axis=1)
    s['title'].replace('', np.nan, inplace=True)
    s.dropna(subset=['title'], inplace=True)
    s.drop(['link', 'href'], axis=1, inplace=True)
    #print(s)
    s.to_csv('bloombergquint.csv', index= False)
    print(s)

except:
    pass
