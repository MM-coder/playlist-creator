import flask, users, music, os
from flask import Flask, redirect, url_for, render_template, request, session, abort, send_file

app = Flask(__name__)
app.secret_key = b"da 10 02 9f 93 50 df ff 08 0b"

# Routes

@app.route('/')
def index():
    users.check_login()
    all_songs =  music.get_all_songs() # So that I don't make 2 dB requests
    return render_template('index.html', all_songs=all_songs, duration=f"{music.get_playlist_duration()}M", number=len(all_songs))

@app.route('/about')
def about():
    users.check_login()
    return render_template('info.html')


@app.route('/add', methods=["GET", "POST"])
def add():
    users.check_login()
    if request.form:
        music.add_song_and_detect_service(str(request.form['url']), session['logged_in']['user'])
        return render_template('add.html', error=False, success=True, successtext="Musica adicionada com sucesso", user_songs=music.get_user_songs(session['logged_in']['user']))
    return render_template('add.html', error=False, success=False, user_songs=music.get_user_songs(session['logged_in']['user']))
    
@app.route('/delete/<name>')
def delete(name):
    users.check_login()
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