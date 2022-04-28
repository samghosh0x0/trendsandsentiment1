from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import numpy as np
url = 'http://profit.ndtv.com/news/latest'

r = requests.get(url)

soup = BeautifulSoup(r.content,  'html.parser')

headline_links = lambda tag: (getattr(tag, 'name', None) == 'a' and 'href' in tag.attrs
                              and 'data-track' not in tag.attrs and 'class' not in tag.attrs
                              and 'alt' not in tag.attrs and 'onclick' not in tag.attrs)
results = soup.find_all(headline_links)
try:
    
    s=pd.DataFrame(results, index=None)
    s.columns = ['link']
    s = s.drop_duplicates(['link'],keep = 'first')
    s.link = s['link'].apply(str)
    s1=s[s['link'].str.contains('http://profit.ndtv.com/news')]
    s2=s1[~s1['link'].str.contains('<img alt="')].reset_index()
    s2.drop(['index'], axis=1, inplace=True)
    s2['link'] = s2['link'].map(lambda x: x.lstrip('<a href='))
    s2.insert(0,'source','http://profit.ndtv.com/news/latest', allow_duplicates=False)
    s2['title'] =s2['link'].str.extract('title=\"(.*?)\"',  expand=True)
    s2['href'] =s2['link'].str.extract('\"(.*?)\"',  expand=True)
    s2['click'] = s2['href']
    s2['title'].replace('', np.nan, inplace=True)
    s2.dropna(subset=['title'], inplace=True)
    s2['title'] = s2['title'].map(lambda x: x.strip())
    s2.drop(['link', 'href'], axis=1, inplace=True)
    s2 = s2.drop_duplicates(['title'],keep = 'first')
    
    s2.to_csv('profit_ndtv.csv', index = False)
    print(s2)
except:
    pass
