from dotenv import load_dotenv
import os
from requests import post, get  # Import the get method
import json
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_secret")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    
    json_result = json.loads(result.content)
    
    if "error" in json_result:
        print(f"Error: {json_result['error_description']}")
        return None

    token = json_result.get("access_token")
    if not token:
        print("Access token not found in the response.")
        return None
    
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}  # Added a space after "Bearer"

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"  # Corrected this line
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    headers = get_auth_header(token)  # Fixed the headers assignment
    result = get(query_url, headers=headers)  # Used the correct get method
    json_result = json.loads(result.content)["artists"]["items"]

    if len(json_result) == 0:
        print("No artist with this name.")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()
if token:
    result = search_for_artist(token, "Shreya Ghoshal")
    if result:
        artist_id = result["id"]
        songs = get_songs_by_artist(token, artist_id)

        for idx, song in enumerate(songs):
            print(f"{idx + 1}. {song['name']}")


