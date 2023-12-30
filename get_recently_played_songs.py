from flask import Flask, request, redirect
import requests
import os

# Assuming you have a config.py file with these variables defined
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

app = Flask(__name__)

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

@app.route('/login')
def login():
    scopes = 'user-read-recently-played'
    auth_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scopes}"
    return redirect(auth_url)

def get_recently_played(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)
    
    if response.status_code == 200:
        tracks = response.json()['items']
        track_list = [f"{idx}. {track['track']['name']} by {track['track']['artists'][0]['name']}" for idx, track in enumerate(tracks, 1)]
        return "\n".join(track_list)
    else:
        return "Failed to fetch recently played tracks."

@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    response = requests.post(TOKEN_URL, data=token_data).json()
    access_token = response.get('access_token')
    
    if access_token:
        tracks_info = get_recently_played(access_token)
        return tracks_info
    else:
        return "Failed to retrieve access token."

if __name__ == '__main__':
    app.run(port=5000)
