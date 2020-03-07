import psycopg2, spotipy, youtube
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyClientCredentials
from youtube import API

url = "postgres://aohxordwzsnidl:0f5b748e243026e102f27babce51623f4350524ca7122606290cc4077c1c7b1e@ec2-54-195-247-108.eu-west-1.compute.amazonaws.com:5432/dcvdo3sgqr2bea"

# Database

result = urlparse(url)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
db = psycopg2.connect(
    database=database,
    user=username,
    password=password,
    host=hostname
)
c = db.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Songs(
                      Name TEXT,
                      Duration INTEGER,
                      SubmittedBy TEXT,
                      AlbumCoverUrl TEXT)""")


## Functions

def add_song_if_not_exists(name: str, duration: int, username: str, cover: str):
    c.execute("SELECT COUNT(*) FROM Songs WHERE Name=%s", (str(name),))
    user_count = c.fetchone()[0]
    if user_count < 1:
        print("[Songs Table] Creating entry  " + str(name))
        c.execute("INSERT INTO Users VALUES (%s, %s, %s, %s)", (str(name), int(duration), str(username), str(cover)))
        db.commit()
    else:
        print("[Songs Table] Didn't add duplicate entry  " + str(name))

# Spotify

## Login
s_client_id = "96a1c7d42a9e47a88c8d467c0d76e0cf"
s_client_secret = "1481031136d342a68cba144c7a983462"
credentials = SpotifyClientCredentials(client_id=s_client_id, client_secret=s_client_secret)
sp = spotipy.Spotify(client_credentials_manager=credentials) # Requires set env variables

## Functions

def add_song_info_from_spotify_url(url: str, username):
    details = dict(sp.track(url))
    name = details['name']
    duration = round(int(details['duration_ms']) / 60000, 2)
    cover_url = details['album']['images'][0]['url']
    add_song_if_not_exists(name, duration, username, cover_url)
    
# Youtube

## login
g_client_id = "724786455286-h797c1jpr7nq4ivsqca73gplkbol5u1c.apps.googleusercontent.com"
g_client_secret = "AxRk4DHa9IfLHd4kDMUXuilQ"
g_key = "AIzaSyDvyloHqIVcizjDdwu0CvTwVvZTGDmrrbE"
g = API(client_id= g_client_id , client_secret= g_client_secret, api_key=g_key)

## Functions


def get_id_from_url(url: str):
    if "youtu.be" in url:
        result = urlparse(url)
        v_id = result.path.replace('/', '')
        return v_id
    else:
        result = urlparse(url)
        v_id = result.query.replace('v=', '')
        return v_id

def add_song_info_from_yt_url(id: str, username: str):
    info = g.get('videos', id=id)
    name = info['items'][0]['snippet']['title']
    cover_url = info['items'][0]['snippet']['thumbnails']['maxres']['url']
    second = g.get('videos', id=id, part="contentDetails") # Youtube only gives duration in a different request, god fuck 'em
    duration = float(second['items'][0]['contentDetails']['duration'].replace('PT', '').replace('S', '').replace('M', '.')) # shitty syntax yes
    add_song_if_not_exists(name, duration, username, cover_url)