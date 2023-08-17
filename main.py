import os
from requests import post, get, delete
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pynput import keyboard


client_id = "user's client id"
client_secret = "user's client secret"
redirect_url = "https://vschac.github.io"
SCOPES = ['user-read-currently-playing', 'playlist-modify-public', 'playlist-read-private']



def make_token(index):
    spotify_oauth = create_spotify_oauth(index)
    token_info = spotify_oauth.get_access_token(code=None, as_dict=True)
    return token_info['access_token']


def create_spotify_oauth(index):
    return SpotifyOAuth(
        client_id = client_id,
        client_secret = client_secret,
        redirect_uri = redirect_url,
        scope=SCOPES[index]
    )



def get_playlists(user_id):
    
    response = get(
        f'https://api.spotify.com/v1/users/{user_id}/playlists',
        headers={
            "Authorization": f"Bearer {tokens['get']}"
        }
    )
    json_resp = response.json()
    print(json_resp)
    return json_resp


def get_current_track_id(token, output: str):

    response = get(
        'https://api.spotify.com/v1/me/player/currently-playing',
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    json_resp = response.json()
    if output == 'id':
        return json_resp['item']['id']
    elif output == 'name':
        return json_resp['item']['name']

def add_to_playlist(playlist_name):
    playlist_id = playlists[playlist_name]
    response = post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris=spotify:track:{get_current_track_id(tokens['read'], 'id')}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tokens['write']}"
            },
            data={
                "uris": [f"spotify:track:{get_current_track_id(tokens['read'], 'id')}"],
                "position": 0
            }
  )


def on_activate_a():
    add_to_playlist(playlist)
    print(f"Added {get_current_track_id(tokens['read'], 'name')} to {playlist}")

def on_activate_q():
  listener.stop()
  print("Listener stopped")

listener = keyboard.GlobalHotKeys({
    '<shift>+a': on_activate_a,
    '<shift>+q': on_activate_q})
listener.start()

if __name__ == "__main__":

  resp = input("Please copy and paste the URL you are directed to into the terminal 3 times. (This is to authenticate all 3 tokens) Type 'OK' to continue ")
  if resp.lower() == 'ok':
    tokens = {'read': make_token(0), 'write': make_token(1), 'get': make_token(2)}
    
  playlists = {
          "skull": "3TUAKz4ZyA4zmq463ZPOFD",
          "hand": "5YlNcpdieJnZAEh3VVCdkd",
          "bomb": "47RHiaJdBqgG59B3kTJEs9",
          "spade": "385RT8POmswXtDI0j0lymn",
          "face": "25vy6ipJ6q8gf1xye34DyA",
          "planet": "1zyzdCUIwG76jNMyD6erDr",
          "rif": "5XoZXc0b3aCB6kQWslTnME",
          "driving": "5Ztl2We2ZUOtRmF89LvDWi",
          "sexy": "0AoDtIfF51GRF7eOebzszV",
          "further-back": "7ADeHu1q2P7KBghwaX4HyO",
          "throwback": "5s8DZdHUy4h0m58KvO4qeX",
          "not-english": "7sPHvrKHzCVCPqghpneUcK",
          "triste": "10r32NN0UnIb8s3prprICV"
      }

  print("These tokens will be valid for one hour before needing to be refreshed")
  playlist = input("Enter playlist name or keyword (Enter 'show all' to view playlist dictionary): ")

  while True:
  
    if playlist == 'show all':
      print(playlists)
      playlist = input("Enter playlist name or keyword (Enter 'show all' to view playlist dictionary): ")

    if playlist in playlists:
      print(f"Selected: {playlist}")
      playlist = input("To select a different playlist type 'quit': ")

    else:
      playlist = input("Playlist not in dictionary, please enter a different name or keyword: ")
    
    if playlist.lower() == 'quit':
      playlist = input("Enter playlist name or keyword (Enter 'show all' to view playlist dictionary): ")
