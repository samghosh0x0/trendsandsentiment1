from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import numpy as np


url = 'http://www.business-standard.com/home-page/'

r = requests.get(url)

soup = BeautifulSoup(r.content,  "html.parser")

headline_links = lambda tag: (getattr(tag, 'name', None) == 'a' and 'href' in tag.attrs
                              )
results = soup.find_all(headline_links)
try :
    s=pd.DataFrame(results, index=None)

    s.columns = ['link']
    s.link = s['link'].apply(str)
    s1 =s[s['link'].str.contains('<a href="/article/')].reset_index()
    s1.drop(['index'], axis=1, inplace=True)
    s1['link'] = s1['link'].map(lambda x: x.lstrip('<a class='))
    s1.insert(0,'source','http://www.business-standard.com', allow_duplicates=False)

    s1['title'] =s1['link'].str.extract('\n(.*?)\<',  expand=True)
    s1['title'] = s1['title'].map(lambda x: x.strip())
    s1= s1.drop_duplicates(['title'],keep = 'first')
    s1['href'] =s1['link'].str.extract('href=\"(.*?)\"',  expand=True)
    s1['title'].replace('', np.nan, inplace=True)
    s1.dropna(subset=['title'], inplace=True)
    s1.dropna(subset=['href'], inplace=True)
    s1['click'] = s1[['source', 'href']].apply(lambda x: ''.join(x), axis=1)
    s1['title'].replace('', np.nan, inplace=True)
    s1.drop(['link', 'href'], axis=1, inplace=True)
    s1.to_csv('business-standard.csv', index= False)
    print(s1)
except:
    pass
