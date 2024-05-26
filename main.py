import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def authenticate_spotify():
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri='http://localhost:9000',
                                                       scope='playlist-modify-public'))
        return sp
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        exit()

def add_song_to_playlist(sp, playlist_id, track_id):
    try:
        current_tracks = sp.playlist_tracks(playlist_id)
        current_track_ids = [item['track']['id'] for item in current_tracks['items']]
        if track_id not in current_track_ids:
            sp.playlist_add_items(playlist_id, [track_id])
            logging.info("Song added successfully to the playlist.")
        else:
            logging.info("Song is already in the playlist. Skipping addition.")
    except Exception as e:
        logging.error(f"Failed to add song to playlist: {e}")

def read_songs_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            songs = [line.strip().split(' by ')[0] for line in file if ' by ' in line]
            return songs
    except Exception as e:
        logging.error(f"Failed to read songs from file: {e}")
        return []

sp = authenticate_spotify()

playlist_name = input("Enter the name of the playlist: ")

playlist = sp.user_playlist_create(sp.me()['id'], playlist_name, public=True)
playlist_id = playlist['id']

file_path = 'songs.txt'
songs = read_songs_from_file(file_path)
for song in songs:
    results = sp.search(q=song, type='track', limit=1)
    
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_id = track['id']
        add_song_to_playlist(sp, playlist_id, track_id)
        print(f"Song '{song}' added to the playlist.")
    else:
        print(f"Song '{song}' not found.")
