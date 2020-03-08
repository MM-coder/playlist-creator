import flask, users, music, hashlib, os
from flask import Flask, redirect, url_for, render_template, request, session, abort, send_file
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = b"da 10 02 9f 93 50 df ff 08 0b"

# Functions

def check_login():
    if 'logged_in' in session:
        return True
    else:
        return abort(401)

def add_song_and_detect_service(url: str, username: str):
    result = urlparse(url)
    if (result.netloc == "www.youtube.com" or  result.netloc == "youtu.be") :
        music.add_song_info_from_yt_id(music.get_id_from_url(url), username)
    elif (result.netloc == "open.spotify.com") :
        music.add_song_info_from_spotify_url(url, username)
    else:
        abort(400)


# Routes

@app.route('/')
def index():
    check_login()
    return render_template('index.html')


@app.route('/add', methods=["GET", "POST"])
def add():
    check_login()
    if request.form:
        add_song_and_detect_service(str(request.form['url']), session['logged_in']['user'])
        return render_template('add.html', error=False, success=True, successtext="Musica adicionada com sucesso", user_songs=music.get_user_songs(session['logged_in']['user']))
    return render_template('add.html', error=False, success=False, user_songs=music.get_user_songs(session['logged_in']['user']))
    
@app.route('/delete/<name>')
def delete(name):
    check_login()
    music.remove_song(name, session['logged_in']['user'])
    return redirect(url_for('add'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.form: # Check if form is request type
        try:
            if users.get_password(request.form['username']) == users.hash_plain_text(request.form['password']): # Compare Password in dB with one provided
                session['logged_in'] = {"user": request.form['username'], "admin": users.get_admin_status(request.form['username'])} # Set local session
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error=True, errortext = "Invalid Username/Password combination! Please try again")
        except:
            return render_template('login.html', error=True, errortext = "We couldn't find that user! Please enter a valid username")
    return render_template('login.html', error=False)


@app.route('/logout')
def logout():
    session.pop('logged_in') # Just Remove everything from session 
    return redirect(url_for('login'))


@app.errorhandler(401)
def handle_401_error(e):
    return render_template('login.html', error=True, errortext = "You need to be logged in to do that! (HTTP error 401)")

@app.errorhandler(400)
def handle_400_error(e):
    return render_template('add.html', error=True, success=False, errortext = "Erro ao adicionar a musica, o link é inválido (HTTP error 400)", user_songs=music.get_user_songs(session['logged_in']['user']))

if __name__ == "__main__":
    app.run()