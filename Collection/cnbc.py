from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import numpy as np

url = 'http://www.cnbc.com/india/'

r = requests.get(url)

soup = BeautifulSoup(r.content,  "html.parser")

headline_links = lambda tag: (getattr(tag, 'name', None) == 'a' and 'href' in tag.attrs
                              and 'data-trknavattr' not in tag.attrs)
results = soup.find_all(headline_links)

try :
    s=pd.DataFrame(results, index=None)
    s.columns = ['link']
    s.link = s['link'].apply(str)
    s1=s[s['link'].str.contains('data-nodeid')]
    s2=s1[~s1['link'].str.contains('video.cnbc.com')].reset_index()
    s2.drop(['index'], axis=1, inplace=True)
    s2.insert(0,'source','http://www.cnbc.com', allow_duplicates=False)
    s2['title'] =s2['link'].str.extract('\n\s*(.*?)\n',  expand=True)
    s2['href'] =s2['link'].str.extract('href=\"(.*?)\"',  expand=True)
    s2['click'] = s2[['source', 'href']].apply(lambda x: ''.join(x), axis=1)
    s2['title'].replace('', np.nan, inplace=True)
    s2.dropna(subset=['title'], inplace=True)
    s2.drop(['link', 'href'], axis=1, inplace=True)
    print(s2)
    s2.to_csv('cnbc.csv', index= False)
    print(s2)

except:
    pass
