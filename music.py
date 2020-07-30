import psycopg2, spotipy, youtube, users, main, zipfile as z, os, youtube_dl
from urllib.parse import urlparse
from spotipy.oauth2 import SpotifyClientCredentials
from youtube import API

# Variables

progress = 0
url = ""

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
                      Duration REAL,
                      SubmittedBy TEXT,
                      AlbumCoverUrl TEXT)""")


## Functions

def add_song_if_not_exists(name: str, duration: int, username: str, cover: str):
    c.execute("SELECT COUNT(*) FROM Songs WHERE Name=%s", (str(name),))
    user_count = c.fetchone()[0]
    if user_count < 1:
        print("[Songs Table] Creating entry  " + str(name))
        c.execute("INSERT INTO Songs VALUES (%s, %s, %s, %s)", (str(name), float(duration), str(username), str(cover)))
        db.commit()
    else:
        print("[Songs Table] Didn't add duplicate entry  " + str(name))

def add_song_and_detect_service(url: str, username: str):
    if users.get_uploaded_number(username) == 5:
        main.abort(429)
    else:
        result = urlparse(url)
        if (result.netloc == "www.youtube.com" or  result.netloc == "youtu.be") :
            add_song_info_from_yt_id(get_id_from_url(url), username)
            users.add_uploaded_number(username)
        elif (result.netloc == "open.spotify.com") :
            add_song_info_from_spotify_url(url, username)
            users.add_uploaded_number(username)
        else:
            main.abort(400)
    

def get_user_songs(username: str):
    c.execute("SELECT * FROM Songs WHERE SubmittedBy=%s", (str(username),))
    songs = c.fetchall()
    return songs

def get_all_songs():
    c.execute("SELECT * FROM Songs")
    songs = c.fetchall()
    return songs
        
def get_song_creator(name: str):
    c.execute("SELECT SubmittedBy FROM Songs WHERE Name=%s", (str(name),))
    name = str(c.fetchone()[0])
    return name

def remove_song(name: str, username: str):
    if get_song_creator(name) == username:
        c.execute("DELETE from Songs WHERE name=%s", (str(name),))
        db.commit()
        users.remove_uploaded_number(username)
        print(f"[Songs Table] Deleted entry {name} by {username}")
    else:
        main.abort(403)

def remove_all_song_from_user(username: str):
    c.execute("DELETE from Songs WHERE SubmittedBy=%s", (str(username),))
    db.commit()
    
def get_id_from_name(name: str):
    r =  g.get('search', q=name)
    return r['items'][0]['id']['videoId']


def get_playlist_duration(): # Shitty Workaround time
    iterable = get_all_songs()
    l = []
    for i in iterable:
        l.append(i[1])
    return sum(l)

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

def add_song_info_from_yt_id(id: str, username: str):
    info = g.get('videos', id=id)
    name = info['items'][0]['snippet']['title']
    try:
        cover_url = info['items'][0]['snippet']['thumbnails']['maxres']['url']
    except KeyError:
        cover_url = info['items'][0]['snippet']['thumbnails']['default']['url']
    second = g.get('videos', id=id, part="contentDetails") # Youtube only gives duration in a different request, god fuck 'em
    duration = float(second['items'][0]['contentDetails']['duration'].replace('PT', '').replace('S', '').replace('M', '.')) # shitty syntax yes
    add_song_if_not_exists(name, duration, username, cover_url)


# Export

def download_mp3_from_id(v_id: str):
    ydl_opts = {
        'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        l = [v_id]
        ydl.download(l)


def get_all_file_paths():
    file_paths = [] 
    directory = "./"
    for root, directories, files in os.walk(directory): 
        for filename in files:
            if 'mp3' in filename:
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath)
    print(directories)
    return file_paths 

def create_zip_file():
    file_paths = get_all_file_paths()
    with z.ZipFile('songs.zip','w') as zip: 
    # writing each file one by one 
        for file in file_paths: 
            zip.write(file) 


def dl_all_songs_and_create_zip():
    global progress
    songs = get_all_songs()
    progress = 10
    for i in songs:
        download_mp3_from_id(get_id_from_name(i))
    progress = 50
    create_zip_file()
    progress = 100