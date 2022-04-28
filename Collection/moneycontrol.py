from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import numpy as np
url = 'http://www.moneycontrol.com/news/'

r = requests.get(url)

soup = BeautifulSoup(r.content,  "html.parser")

headline_links = lambda tag: (getattr(tag, 'name', None) == 'a' and 'href' in tag.attrs
                              and 'class' not in tag.attrs
                              and 'alt' not in tag.attrs and 'onclick' not in tag.attrs)
results = soup.find_all(headline_links)
try :
    #print(results)
    s=pd.DataFrame(results, index=None)
    s.columns = ['link']
    s.link = s['link'].apply(str)
    s1=s[s['link'].str.contains('http://www.moneycontrol.com/news/')]
    s2=s1[~(s1['link'].str.contains('"http://www.moneycontrol.com/news/"'))]
    s3=s2[~(s2['link'].str.contains('news/businessline'))]
    s4=s3[~(s3['link'].str.contains('news/skymetweather'))]
    s5=s4[~(s4['link'].str.contains('/jones-lang-lasalle'))]
    s6=s5[~(s5['link'].str.contains('/knight-frank'))]
    s7=s6[~(s6['link'].str.contains('/makaan'))]
    s8=s7[~(s7['link'].str.contains('/sulekha'))]
    s9=s8[~(s8['link'].str.contains('target="_blank"'))]
    s10=s9[~(s9['link'].str.contains('title="Site Map"'))].reset_index()
    s10.drop(['index'], axis=1, inplace=True)
    s10['link'] = s10['link'].map(lambda x: x.lstrip('<a href='))
    s10.insert(0,'source','http://www.moneycontrol.com/news/', allow_duplicates=False)
    s10['title'] =s10['link'].str.extract('title=\"(.*?)\"',  expand=True)
    s10['href'] =s10['link'].str.extract('\"(.*?)\"',  expand=True)
    s10['click'] = s10['href']
    s10['title'].replace('', np.nan, inplace=True)
    s10.dropna(subset=['title'], inplace=True)
    s10.drop(['link', 'href'], axis=1, inplace=True)
    s10.to_csv('moneycontrol.csv', index = False)
    print(s10)
    
except:
    pass
