from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from urllib.parse import urlencode

#authenticate API
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = "https://localhost:8000/callback"
SCOPE = 'user-read-currently-playing'

#print(client_id, client_secret)

def get_cc_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

auth_params = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': redirect_url,
    'scope': SCOPE
}

auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(auth_params)
print(f'Visit this URL to authorize your app: {auth_url}')

def get_access_token(auth_code: str):
    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": "https://localhost:8000/callback",
        },
        #auth=(client_id, client_secret),
    )
    access_token = response.json()["access_token"]
    return access_token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



def get_current_track(token):
    track_url = 'https://api.spotify.com/v1/me/player/currently-playing'
    response = get(track_url, headers=get_auth_header(token))
    resp_json = response.json()

    
    return resp_json

#token = get_cc_token()
#print(token)