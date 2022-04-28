import nltk
#from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
from pandas import DataFrame
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tag.stanford import StanfordPOSTagger
from nltk.internals import find_jars_within_path
import csv
import numpy as np
from nltk.tokenize import MWETokenizer
import sqlalchemy
import sent_mod as sent
#import untokenize
import re
import os


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
                   'Ourselves', 'Each', 'Haven', 'Your', 'Sons', 'sons', 'Hits', 'Going', 'X', 'Stay','Says', '?s', "'s"  ])

stop_words_lower = [word.lower() for word in stop_words]

#importing the csv data
path  = "../Collection/all_newsind.csv"
ind_headlines_data = pd.read_csv(path, encoding = "ISO-8859-1")
#print(stop_words)
#cimpiling the headlines in one paragraph
ind_headlines=ind_headlines_data[['title']].copy()

ind_headlines['title'].str.join('. ')
complied_text=ind_headlines['title'].str.cat(sep='.')

#Word tokenizing
word_tokenized = tokenizer.tokenize(complied_text.split())
word_lemas = [(lemmatizer.lemmatize(w)) for (w) in word_tokenized]


###Using Standford tagger
##model = '/usr/lib/python3.5/Lib/stanford-postagger-2015-04-20/models/english-bidirectional-distsim.tagger'
##jar = 'C:/Users/Administrator/AppData/Local/Programs/Python/Python35-32/Lib/stanford-postagger-2015-04-20/stanford-postagger.jar'
##java_path = 'C:/Program Files/Java/jre1.8.0_112/bin/java.exe'
##os.environ['JAVAHOME'] = java_path
##tagger = StanfordPOSTagger(model, path_to_jar=jar, encoding = 'utf8', java_options = '-mx4096m')
##word_tokenized_pos = tagger.tag(word_lemas)

word_tokenized_pos = nltk.pos_tag(word_lemas)

#eliminating stop words
filtered_sentence = [w for w in word_tokenized if not w in stop_words]
filtered_sentence1 = [w for w in filtered_sentence if not w in stop_words_lower]
filtered_sentence2 = [w for w in filtered_sentence1 if not '.' in w]
filtered_sentence3 = [w for w in filtered_sentence2 if not len(w)==1]
filtered_sentence4 = [w for w in filtered_sentence3 if not "'" in w]
filtered_sentence5 = [w for w in filtered_sentence4 if not "?" in w]
filtered_sentence6 = [w for w in filtered_sentence5 if not "&" in w]

#finding proper nous in the tokenized words
nouns = [token for token, pos in pos_tag(filtered_sentence6) if pos.startswith('NNP')]
nouns = nltk.FreqDist(nouns)


#most common nouns
trends = nouns.most_common(10)
trends_pd = pd.DataFrame(trends, columns =['word', 'frequency'])
print(trends_pd)

#Finding out the trending words and the links to the articles
trendlist = trends_pd['word'].tolist()
array_length1 = len(trendlist)
trend_frame1 = []
trend_frame2 = []
ind_headlines_data.title = ind_headlines_data['title'].apply(str)
appended_data = []
for x in range(array_length1):
    trend_frame1.append(ind_headlines_data[ind_headlines_data['title'].str.contains(trendlist[x])])
    trend_frame2.append(trendlist[x])
           

trend_frame2_pd = pd.DataFrame(trend_frame2)
trendlink_df = pd.concat(trend_frame1).reset_index()
trendlink_df.drop(['index'], axis=1, inplace=True)

trending = []
for s in range(array_length1):
    for t in range(len(trend_frame1[s])):
        trending.append(trendlist[s])
        
trending_df = pd.DataFrame(trending)

trending_df.columns = ['Keyword']
trend_to_save = pd.concat([trendlink_df, trending_df], axis=1, join_axes=[trending_df.index])
trend_to_save["filter"] = trend_to_save["Keyword"].map(str) + trend_to_save["click"]
trend_to_save = trend_to_save.drop_duplicates('filter',  keep='first')
trend_to_save.drop(['filter'], axis=1, inplace=True)
trend_to_save = trend_to_save[['Keyword', 'source', 'title', 'click', 'Timelog']]


trend_to_save_gr=trend_to_save.groupby(['Keyword']).agg(lambda x: '. '.join(set(x)))
trend_to_save_pd = pd. DataFrame(trend_to_save_gr)
trend_to_save_pd['tokenized'] = trend_to_save_pd.apply(lambda row: tokenizer.tokenize(row['title'].split()), axis=1)
trend_to_save_pd.title = trend_to_save_pd['title'].apply(str)

trend_to_save_pd['tokenized'] = trend_to_save_pd['tokenized'].apply(lambda x: [w for w in x if w not in stop_words])
trend_to_save_pd['tokenized'] = trend_to_save_pd['tokenized'].apply(lambda x: [w for w in x if w not in stop_words_lower])
trend_to_save_pd['tokenized'] = trend_to_save_pd['tokenized'].apply(lambda x: [lemmatizer.lemmatize(w) for (w) in x])
#trend_to_save_pd['tokenized'] = trend_to_save_pd.apply(lambda row: tagger.tag(row['tokenized']), axis=1)
trend_to_save_pd['tokenized'] = trend_to_save_pd.apply(lambda row: nltk.pos_tag(row['tokenized']), axis=1)


allowed_word_types = ["JJ", "JJR", "JJS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "RB", "RBR", "RBS"]

trend_to_save_pd['tokenized_filtered'] = trend_to_save_pd['tokenized'].apply(lambda x: [w for w in x if w[1] in allowed_word_types])



def unzip(words):
        x = zip(*words)
        unzipped = list(x)[0]
        return unzipped


trend_to_save_pd.drop(['source', 'title', 'click'], axis=1, inplace=True)
trend_to_save_pd['unzipped'] = trend_to_save_pd.apply(lambda row: unzip(row['tokenized']), axis=1)

trend_to_save_pd['untokenized'] = trend_to_save_pd['unzipped'].apply(lambda x:' '.join(x))
trend_to_save_pd1 = trend_to_save_pd.dropna(axis=1, how='any')
trend_to_save_pd1.drop(['tokenized', 'tokenized_filtered', 'unzipped'], axis=1, inplace=True)

sentiment_set = []
  

for t in range(len(trend_to_save_pd1)):
    sentiment_set.append(sent.sentiment(trend_to_save_pd1.untokenized[t]))


trend_to_save_pd1.drop(['untokenized'], axis=1, inplace=True)
trend_to_save_pd1 = trend_to_save_pd1.reset_index()
sentiment_pd = pd.DataFrame(sentiment_set)
sentiment_pd.columns = ['sentiment', 'confidence']


#saving to sql

###Connecting to MySQL
##eng = sqlalchemy.create_engine("mysql+pymysql://root:xxx@xxx/xxx")

#saving the trending words to mysql

trendlist_withsentiment = pd.concat([trend_to_save_pd1, sentiment_pd],axis=1, join_axes=[trend_to_save_pd1.index])
trends_pd_az = trends_pd.sort_values(['word'], ascending = [True])
trends_pd_az.columns = ['Keyword', 'frequency']
trendlist_df = pd.merge(trendlist_withsentiment, trends_pd_az, on='Keyword', how='outer')
trendlist_df = trendlist_df.sort_values(['frequency'], ascending = [False])
trendlist_df = trendlist_df.reset_index()
trendlist_df.drop(['index'], axis=1, inplace=True)
trendlist_df = trendlist_df[['Keyword', 'frequency', 'sentiment', 'confidence', 'Timelog']]
print(trendlist_df)

##if (len(trendlist_df)>0):
##    trendlist_df.to_sql(name='news_indian_trendingkeys', con=eng, if_exists = 'replace', index=True)
##    with open('ind_trendlist.csv', 'w') as f:
##        trendlist_df.to_csv(f, header=False)
    
###saving the links to the trending words
##if (len(trend_to_save)>0):
##    trend_to_save.to_sql(name='news_indian_trendlinks', con=eng, if_exists = 'replace', index=True)
##    with open('ind_trends_to_save.csv', 'w') as f:
##        trend_to_save.to_csv(f, header=False)    
    

##        
###closing the MySQL connection
##eng.dispose()
