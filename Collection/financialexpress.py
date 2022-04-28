from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import numpy as np
url = 'http://www.financialexpress.com/'

r = requests.get(url)

soup = BeautifulSoup(r.content,  "html.parser")

headline_links = lambda tag: (getattr(tag, 'name', None) == 'a' and 'href' in tag.attrs
                              and 'class' not in tag.attrs)

results = soup.find_all(headline_links)
try:
    s=pd.DataFrame(results, index=None)
    s.columns = ['link']
    s.link = s['link'].apply(str)
    s1a =s[s['link'].str.contains('http://www.financialexpress.com/economy/')]
    s1b =s[s['link'].str.contains('http://www.financialexpress.com/india-news/')]
    s1c =s[s['link'].str.contains('http://www.financialexpress.com/opinion/')]
    s1d =s[s['link'].str.contains('http://www.financialexpress.com/industry/')]
    s1e =s[s['link'].str.contains('http://www.financialexpress.com/money/')]
    s1f =s[s['link'].str.contains('http://www.financialexpress.com/market/')]
    s1g =s[s['link'].str.contains('http://www.financialexpress.com/technology/')]
    s1h =s[s['link'].str.contains('http://www.financialexpress.com/world-news/')]
    frames = [s1a, s1b, s1c, s1d, s1e, s1f, s1g, s1h]
    s1 = pd.concat(frames).reset_index()
    s1.drop(['index'], axis=1, inplace=True)
    s1['link'] = s1['link'].map(lambda x: x.lstrip('<a class='))
    s1.insert(0,'source','http://www.financialexpress.com', allow_duplicates=False)
    s2 =s1[s1['link'].str.contains('title="')].reset_index()
    s2.drop(['index'], axis=1, inplace=True)
    s2['title'] =s2['link'].str.extract('title=\"(.*?)\"',  expand=True)
    s2['href'] =s2['link'].str.extract('href=\"(.*?)\"',  expand=True)
    s2['click'] = s2['href']
    s2['title'].replace('', np.nan, inplace=True)
    s2.dropna(subset=['title'], inplace=True)
    s2.drop(['link', 'href'], axis=1, inplace=True)
    print(s2)
    s2.to_csv('financialexpress.csv', index = False)
    print(s2)
except:
    pass
