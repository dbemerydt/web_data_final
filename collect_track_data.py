import pandas as pd
import requests
import lyricsgenius
from bs4 import BeautifulSoup
import time
import numpy as np
from random import random
import os
import string
import pickle
from glob import glob
import time
from sys import argv
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius

start_idx = 0
start_idx = int(argv[1])

with open('../assignment-03/spotify_creds.pkl', 'rb') as handle:
    spotify_creds = pickle.load(handle)
    
manager = SpotifyClientCredentials(
    client_id = spotify_creds['client_id'],
    client_secret = spotify_creds['client_secret']
)

sp = spotipy.Spotify(client_credentials_manager = manager)

    
with open('../assignment-03/genius_creds.pkl', 'rb') as handle:
    genius_creds = pickle.load(handle)
    
ACCESS_TOKEN = genius_creds['ACCESS_TOKEN'] 
API_BASE_URL = genius_creds['API_BASE_URL'] 
CLIENT_SECRET = genius_creds['CLIENT_SECRET'] 
REDIRECT_URI = genius_creds['REDIRECT_URI']

genius = lyricsgenius.Genius(ACCESS_TOKEN,timeout=50)

weekly_200_df = pd.read_csv('data/weekly_200_df_2022.csv')
all_tracks = weekly_200_df.stack().unique()
word_scores = pd.read_csv('../final_project/data/ousiometry_data_augmented.tsv', sep='\t', header=0)

if start_idx == 0:
    track_data = pd.read_csv('data/track_data-2022.csv')
    # track_data = pd.DataFrame(index = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    #        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
    #        'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms',
    #        'time_signature', 'scored_words', 'valence', 'arousal', 'dominance', 'goodness',
    #        'energy', 'structure', 'power', 'danger'])
else:
    track_data = pd.read_csv('data/track_data-2022.csv')

print('total unique tracks: '+str(len(all_tracks)))
for i,track in enumerate(all_tracks[start_idx:]):
    i+=start_idx
    time.sleep(random()*3+random())
    print('track '+str(i+1))
    if i % 5 == 0:
        sp = spotipy.Spotify(client_credentials_manager = manager)
        genius = lyricsgenius.Genius(ACCESS_TOKEN,timeout=50)


    track_search = sp.search(track.split(',')[0],type='track')
    track_id = track_search['tracks']['items'][0]['id']
    audio_features = sp.audio_features(track_id)[0]
    

    track_name = track.split('---')[0].split(' - ')[0].split(' (ft')[0].split(' (feat')[0].split(' (with')[0].split(' (From the Original Motion Picture')[0].replace(' (Remastered)','').replace('N****','NIGGA').replace(' (League of Legends Worlds Anthem)','') #ugh
    artist_name = track.split('---')[1].split(',')[0].split(' - ')[0] 
    song_object = genius.search_song(title=track_name,artist=artist_name)

    annotations = genius.song_annotations(song_id=song_object.id)
    response = requests.get(song_object._body['url'])
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(re.escape('SongDescription__Content'))
    elements = soup.find_all(class_=pattern)

    # I heard you like list comprehension
    if len(elements)>0:
        list_of_annotations = [elements[0].text]+[a for la in [[item for sublist in entry[1] for item in sublist] for entry in annotations] for a in la]
    else:
        list_of_annotations = [a for la in [[item for sublist in entry[1] for item in sublist] for entry in annotations] for a in la]



    track_annotations = '\n\n'.join(list_of_annotations)
    df = pd.DataFrame(columns = word_scores.columns)

    ousio_df = pd.DataFrame(columns = word_scores.columns)
    for word in track_annotations.translate(str.maketrans('', '', string.punctuation)).replace('\n',' ').replace('’',"'").lower().split(' '):
        ousio_df = pd.concat([ousio_df,word_scores[word_scores['word']==word]])

    audio_features['scored_words'] = len(ousio_df)
    print('_'+str(len(ousio_df))+' scored words')

    track_data[track] = pd.concat([pd.Series(audio_features),ousio_df[ousio_df.columns[1:]].mean()]).tolist()

    track_data.to_csv('data/track_data-2022.csv',index=False)






















