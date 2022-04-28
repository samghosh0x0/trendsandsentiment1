from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import numpy as np
url = 'http://www.livemint.com/'

r = requests.get(url)

soup = BeautifulSoup(r.content,  "html.parser")

headline_links = lambda tag: (getattr(tag, 'name', None) == 'a' and 'href' in tag.attrs
                              and 'class' not in tag.attrs)
results = soup.find_all(headline_links)
try:
    s=pd.DataFrame(results, index=None)
    s.columns = ['link']
    s.link = s['link'].apply(str)
    s1a =s[s['link'].str.contains('<a href="/Industry/')]
    s1b =s[s['link'].str.contains('<a href="/Opinion/')]
    s1c =s[s['link'].str.contains('<a href="/Companies/')]
    s1d =s[s['link'].str.contains('<a href="/Politics/')]
    s1e =s[s['link'].str.contains('<a href="/Money/')]
    frames = [s1a, s1b, s1c, s1d, s1e]
    s1 = pd.concat(frames)
    s2=s1[s1['link'].str.contains('title="')]
    s3=s2[~s2['link'].str.contains('<img alt=')].reset_index()
    s3.drop(['index'], axis=1, inplace=True)
    s3.insert(0,'source','http://www.livemint.com', allow_duplicates=False)
    s3['title'] =s3['link'].str.extract('title=\"(.*?)\"',  expand=True)
    s3['href'] =s3['link'].str.extract('href=\"(.*?)\"',  expand=True)
    s3['click'] = s3[['source', 'href']].apply(lambda x: ''.join(x), axis=1)
    s3['title'].replace('', np.nan, inplace=True)
    s3.dropna(subset=['title'], inplace=True)
    s3.drop(['link', 'href'], axis=1, inplace=True)
    s3.to_csv('livemint.csv', index = False)
    print(s3)
except:
    pass
