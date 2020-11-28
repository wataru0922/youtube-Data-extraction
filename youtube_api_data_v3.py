# -*- coding: utf-8 -*-
"""Youtube API data v3

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kvFNCQj0vZQf0tEQAidvrHTEKQ5zfTs6
"""

from apiclient.discovery import build
import pandas as pd

YOUTUBE_API_KEY = 'AIzaSyCjoIwe4qnJoEXy8_f9kKjougqdXA41cHE'

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

dic_list = []
search_response = youtube.search().list(part='snippet',q="野良猫",order="viewCount",type='video')
output = youtube.search().list(part='snippet',q="検索ワード",order="viewCount",type='video').execute()

#一度に5件しか取得できないため何度も繰り返して実行
for i in range(100):
  dic_list = dic_list + output['items']
  search_response = youtube.search().list_next(search_response, output)
  output = search_response.execute()
  
df = pd.DataFrame(dic_list)
#各動画毎に一意のvideoIdを取得
df1 = pd.DataFrame(list(df['id']))['videoId']
#各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
df2 = pd.DataFrame(list(df['snippet']))[['channelTitle','publishedAt','channelId','title','description']]
ddf = pd.concat([df1,df2], axis = 1)

def get_statistics(id):
    statistics = youtube.videos().list(part = 'statistics', id = id).execute()['items'][0]['statistics']
    return statistics

df_static = pd.DataFrame(list(ddf['videoId'].apply(lambda x : get_statistics(x))))

df_output = pd.concat([ddf,df_static], axis = 1)

df_output['video_url']='https://www.youtube.com/watch?v='+ddf['videoId']
df_output['channelTitle_url']='https://www.youtube.com/channel/'+ddf['channelId']

df_output.rename(columns={'publishedAt':'投稿日','channelTitle':'チャンネル名','title':'タイトル','viewCount':'再生回数','video_url':'URL','channelTitle_url':'チャンネルURL'},inplace=True)

df_output=df_output.drop(['videoId','channelId','description','likeCount','dislikeCount','favoriteCount','commentCount'],axis='columns')

df_output

!pip install xlwt
!pip install openpyxl

import openpyxl
df_output.to_excel('ファイル名.xlsx',sheet_name='new_sheet_name')

from google.colab import files
files.download('ファイル名.xlsx')