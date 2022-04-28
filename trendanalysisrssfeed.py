import feedparser
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import pandas as pd
from pandas import DataFrame
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import csv
import numpy as np
from nltk.tokenize import MWETokenizer
import sqlalchemy
import re
import os
from datetime import datetime, time, timedelta
from dateutil import parser as date_parser

from string import printable
st = set(printable)

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


##local
data = pd.read_csv("source.csv")


###Connecting to MySQL

eng = sqlalchemy.create_engine("mysql+pymysql://email:xxxx@xxxx/xxx?charset=utf8", execution_options={"sqlite_raw_colnames": True})


connection = eng.raw_connection()
cur=connection.cursor()

sql_latest = "SELECT * FROM news_indian_trendlinks ORDER BY key1 DESC LIMIT 1"

cur.execute(sql_latest)

result_set = cur.fetchall()

if not result_set:
    midnight = datetime.combine(datetime.today(), time.min)
    last_entry_datetime = midnight
else:
    last_entry_datetime = date_parser.parse(result_set[-1][-2])

rawrss = data['RSS'].head(600).tolist()


feeds = [] # list of feed objects
for url in rawrss:
    try:
        f = feedparser.parse(url)
        feeds.append(f)
    except:
        pass

print(len(feeds))
if (len(feeds)>0):
    posts = []
    for feed in feeds:
        for post in feed.entries:
            try:
                if((date_parser.parse(post.published)).replace(tzinfo=None) > last_entry_datetime):
                    posts.append((post.title, post.link, post.summary, (date_parser.parse(post.published).replace(tzinfo=None)).strftime('%Y-%m-%d %H:%M:%S')))
            except:
                pass

    print(len(posts))
    if (len(posts)>0):
        df = pd.DataFrame(posts, columns=['title', 'click1', 'summary', 'Timelog']) # pass data to init
        ##print(len(df))
        df = df[df['title'].str.contains("[a-zA-Z]").fillna(False)]
        ##print(len(df))
        df.drop_duplicates(subset=['click1'], keep=False)
        
        df['source'] = df['click1'].str.split('//', 1).str[1].str.strip()

        df['source'] = df['source'].str.split('/').str[0]

        df['click1'].str.strip()

        df['click'] = df['click1'].str.split(" ", 1).str[0]

        df.drop(['click1'], axis=1, inplace=True)

        ##print(len(df))
        lemmatizer = WordNetLemmatizer()
        tokenizer = MWETokenizer()
        tokenizer = MWETokenizer([('a', 'little'), ('a', 'little', 'bit'), ('a', 'lot')])
        tokenizer.add_mwe(('in', 'spite', 'of'))

        #defining stop words
        stop_words = set(stopwords.words('english'))
        stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']',
                           '{', '}', "'s", 'Rs', 'Should', 'Ve', 'Above', 'The', ',',
                           'But', 'We', 'Re', 'Herself', 'After', ':', 'Himself', 'Too',
                           'Can', 'Any', 'You', 'Own', 'Most', 'Up', 'Again', 'Hasn',
                           'Themselves', 'Not', 'Does', 'Did', 'Yourself',
                           'Then', 'An', 'When', 'Be', 'Myself', 'Doesn', 'Isn', 'Once',
                           'Having', 'If', 'Its', 'Nor', 'Them', 'Between', 'Which',
                           'Hers', 'Couldn', 'Here', 'M', 'Below', 'Wasn', 'Wouldn',
                           'Was', 'I', 'O', 'About', 'Down', 'Her', 'So', 'Only', 'Both',
                           'Than', 'Ma', 'D', 'Other', 'Over', 'It', 'Me', 'While',
                           'Of', 'During', 'In', 'Before', 'Out', 'Yourselves', 'Who',
                           'Under', 'Whom', 'A', 'Had', 'Ain', 'What', 'Those', 'Aren', 'This',
                           'Mustn', 'Needn', 'Our', 'Being', 'Doing', 'Into', 'Don', 'With',
                           'Is', 'LL', 'Off', 'His', 'Against', 'Y', '}', 'Won', 'Some', 'There',
                           'Their', 'For', 'Were', 'Have', 'Very', 'Will', 'He', 'Few', 'That',
                           'Just', 'Until', 'Why', 'Same', 'Mightn', 'On', 'Theirs', 'Yours', 'Are',
                           'To', 'Him', 'Do', 'She', 'From', 'My', 'How', 'Such', 'They', 'And',
                           'Has', 'Through', 'By', 'Hadn', 'Now', 'These', 'Ours', 'All', 'Weren',
                           'More', 'Am', 'Itself', 'Didn', 'Been', 'As', 'No',
                           'Shouldn', 'Further', 'Or', '!', 'Where', 'S', 'Because', 'Shan', 'At',
                           'Ourselves', 'Each', 'Haven', 'Your', 'Sons', 'sons', 'Hits', 'Going', 'X', 'Stay','Says', '?s', "'s", "BS"  ])

        stop_words_lower = [word.lower() for word in stop_words]

        headlines= df[['title']].copy()



        headlines['title'].str.join('. ')
        complied_text=headlines['title'].str.cat(sep='.')

        #Word tokenizing
        word_tokenized = tokenizer.tokenize(complied_text.split())
        word_lemas = [(lemmatizer.lemmatize(w)) for (w) in word_tokenized]

        ##word_tokenized_pos = myTagger.tag(word_lemas)
        word_tokenized_pos = nltk.pos_tag(word_lemas)

        #eliminating stop words
        filtered_sentence = [w for w in word_tokenized if not w in stop_words]
        filtered_sentence1 = [w for w in filtered_sentence if not w in stop_words_lower]
        filtered_sentence2 = [w for w in filtered_sentence1 if not '.' in w]
        filtered_sentence3 = [w for w in filtered_sentence2 if len(w) > 2]
        filtered_sentence4 = [w for w in filtered_sentence3 if not "'" in w]
        filtered_sentence5 = [w for w in filtered_sentence4 if not "?" in w]
        filtered_sentence6 = [w for w in filtered_sentence5 if not "&" in w]

        #finding proper nous in the tokenized words
        nouns = [token for token, pos in pos_tag(filtered_sentence6) if pos.startswith('NNP')]
        nouns1 = nltk.FreqDist(nouns)


        #most common nouns
        trends = nouns1.most_common(10)
        trend_whole = nouns
        
        trends_pd = pd.DataFrame(trends, columns =['word', 'frequency'])
        trends_pd_whole = pd.DataFrame(trend_whole, columns =['word'])
        trends_pd["word"] = trends_pd['word'].str.replace('[^\w\s]','')
        trends_pd["word"] = trends_pd['word'].apply(lambda x: ''.join([" " if  i not in  st else i for i in x]))

        trends_pd_whole["word"] = trends_pd_whole['word'].str.replace('[^\w\s]','')
        trends_pd_whole["word"] = trends_pd_whole['word'].apply(lambda x: ''.join([" " if  i not in  st else i for i in x]))
        #Finding out the trending words and the links to the articles
        trendlist = trends_pd['word'].tolist()
        trendlist_whole = trends_pd_whole['word'].tolist()
        
        
        array_length1 = len(trendlist)
        array_length1_whole = len(trendlist_whole)

        trend_frame1 = []
        trend_frame2 = []



        df.title = df['title'].apply(str)
        


        appended_data = []
        for x in range(array_length1_whole):
            trend_frame1.append(df[df['title'].str.contains(trendlist_whole[x])])
            trend_frame2.append(trendlist_whole[x])

        ##print(len(trend_frame1))
        trendlink_df = pd.concat(trend_frame1).reset_index()
        trendlink_df.drop(['index'], axis=1, inplace=True)


        trending = []
        for s in range(array_length1_whole):
            for t in range(len(trend_frame1[s])):
                trending.append(trendlist_whole[s])
                
        trending_df = pd.DataFrame(trending)
        

        trending_df.columns = ['Keyword']
        trend_to_save = pd.concat([trendlink_df, trending_df], axis=1, join_axes=[trending_df.index])



        trend_to_save["filter"] = trend_to_save["Keyword"].map(str) + trend_to_save["click"]
        trend_to_save = trend_to_save.drop_duplicates('filter',  keep='first')
        trend_to_save.drop(['filter'], axis=1, inplace=True)


        trend_to_save = trend_to_save[['Keyword', 'source', 'title','summary', 'click', 'Timelog']]


        trend_to_save_pd = pd. DataFrame(trend_to_save)
        trend_to_save_pd['tokenized'] = trend_to_save_pd.apply(lambda row: tokenizer.tokenize(row['title'].split()), axis=1)
        trend_to_save_pd.title = trend_to_save_pd['title'].apply(str)

        trend_to_save_pd1 = trend_to_save_pd.dropna(axis=1, how='any')


        trend_to_save_pd1 = trend_to_save_pd1.reset_index()

        trend_to_save_pd1["title"] = trend_to_save_pd1['title'].str.replace('"',"'")
        trend_to_save_pd1["summary"] = trend_to_save_pd1['summary'].str.replace('"',"'")
        trend_to_save_pd1["click"] = trend_to_save_pd1['click'].str.replace(' ',"")


        trend_to_save_pd1["title"] = trend_to_save_pd1['title'].apply(lambda x: ''.join([" " if  i not in  st else i for i in x]))
        trend_to_save_pd1["summary"] = trend_to_save_pd1['summary'].apply(lambda x: ''.join([" " if  i not in  st else i for i in x]))
        trend_to_save_pd1["click"] = trend_to_save_pd1['click'].apply(lambda x: ''.join([" " if  i not in  st else i for i in x]))

        trend_to_save_pd1['title'] = trend_to_save_pd1['title'].apply(lambda x: remove_html_tags(x))
        trend_to_save_pd1['summary'] = trend_to_save_pd1['summary'].apply(lambda x: remove_html_tags(x))

        trend_to_save_pd1['title'] = trend_to_save_pd1['title'].apply(lambda x: x.encode('utf-8', 'surrogateescape').decode('utf-8'))
        trend_to_save_pd1['summary'] = trend_to_save_pd1['summary'].apply(lambda x: x.encode('utf-8', 'surrogateescape').decode('utf-8'))
        ##print(len(trends_pd))
        ##print(len(trend_to_save_pd1))

        #saving the the trending words
        if (len(trends_pd)>0):
            
            trends_pd.to_sql(name='news_indian_trendingkeys', con=eng, if_exists = 'replace', index=True)

        #saving the links to the trending words
        if (len(trend_to_save_pd1)>0):
            for index, row in trend_to_save_pd1.iterrows():
                try:
                    cur.execute('SELECT * FROM news_indian_trendlinks where click LIKE "%s" LIMIT 1'%(row['click']))
                    result = cur.fetchone()
                    if result is None:
                        sql_enter= """INSERT INTO news_indian_trendlinks (Keyword, source, title, summary, click, Timelog)
                                VALUES ("%s","%s", "%s", "%s", "%s","%s")"""%(row['Keyword'], row['source'], row['title'], row['summary'], row['click'], row['Timelog'])

                        cur.execute(sql_enter)
                        connection.commit()
                except:
                    pass

                
        #closing the MySQL connection
        eng.dispose()




