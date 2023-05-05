"""           
Backend Code for CS411
API 1: RAWG Video Game Database
API 2: 
"""

import flask
from flask import Flask, Response, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
import flask_login
from flask_oauthlib.client import OAuth
import requests
from flask_restful import Api, Resource, reqparse
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import threading
#for image uploading
import os, base64

# generate a self-signed SSL certificate
os.system('openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.key')

mysql = MySQL()
app = Flask(__name__)
app.debug = True
app.secret_key = 'secret_for_safety'  

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'CS460460@'
app.config['MYSQL_DATABASE_DB'] = 'gamerank'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#OAuth Login
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key= '896340764856-3peefrs8fufonvq06ke5ak9662sfhaob.apps.googleusercontent.com',
    consumer_secret= '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',
    request_token_params={'scope': 'email'},
    base_url = 'https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url = 'https://oauth2.googleapis.com/token',
    authorize_url="https://accounts.google.com/o/oauth2/auth",
)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

##################################################################################################
# Set up Spotify API credentials to have music playing while the code is running

def run_spotify_playback():
    # Set up Spotify API credentials
    redirect_uri = 'http://127.0.0.1:7000/callback'
    client_id = 'b9af3eb4f88d4a95bd4776ccc1129d18'
    client_secret = 'c4d715e23a85463d855c3f52872c829c'
    # Set up authentication
    scope = 'user-modify-playback-state user-read-playback-state'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    # Search for the song you want to play on a loop
    results = sp.search(q='Gaming Lofi', type='track', limit=1)
    uri = results['tracks']['items'][0]['uri']
    
    while True:
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            # Play the song on the specified device
            sp.start_playback(device_id=device_id, uris=[uri], context_uri=None, offset=None)
            print('Playing "Objects in the Mirror" on device ID:', device_id)
            time.sleep(3600) # play for 1 hour before stopping
        else:
            print('No devices found. Trying again in 5 seconds...')
            time.sleep(5)

# start the Spotify playback in a separate thread
spotify_thread = threading.Thread(target=run_spotify_playback)
spotify_thread.start()

###############################################################################################
def insertAllGames(g_list):
    for i in g_list:    
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO recs (rec_game_name) VALUES (%s)", (i,))
        conn.commit()
#############################################################################################

def getAllGames():
    cursor = conn.cursor()
    cursor.execute("SELECT game_name FROM User_Games")
    return cursor.fetchall()

#################################################################################################
def replace_space(gname):
    new_name = ''
    for i in range(len(gname)):
        if gname[i] == ' ':
            new_name += '-'
        else:
            new_name += gname[i]
    return str(new_name)
#################################################################################################################
#game id cap number #949995
# Gaming database to pull game info from
def game(gname):
    name = gname
    url = "https://rawg-video-games-database.p.rapidapi.com/games/" + name + "?key=2f70e298b9ba477e80cc87048455f30a"
    
    headers = {
            	"X-RapidAPI-Key": "7740c2a325msh0911c68659b1739p1f47f3jsn641fd99e2bf0",
            	"X-RapidAPI-Host": "rawg-video-games-database.p.rapidapi.com"
            }
    
    response = requests.request("GET", url, headers=headers)
    y = json.loads(response.text)
    user_game = y
    #assume that the input is a string that is also a game that exists in the database
    user_game_genres = user_game["genres"] 
    user_game_id = y["id"] 
    user_genre_list = []
    
    #outputs the genre list of the user inputted game
    for i in range(len(user_game_genres)):
        user_genre_list += [user_game_genres[i]["name"]]
    
    #calls the api again to extract the name of a game given an arbitrary game id number. 
    same_genre_list = []
    final_list = []
    counter = 0
    while len(same_genre_list) < 3:
        try:
            counter += 1
            x = str(user_game_id + counter)
            url = "https://rawg-video-games-database.p.rapidapi.com/games/" + x + "?key=2f70e298b9ba477e80cc87048455f30a"
            new_response = requests.request("GET", url, headers=headers)
            new_game = json.loads(new_response.text)
            
            #outputs the genre list of the iterated game
            new_game_genres = new_game["genres"]
            new_game_id = new_game['id']
            new_genre_list = []
            for i in range(len(new_game_genres)):
                new_genre_list += [new_game_genres[i]['name']]
    
            match_count = 0
            for a in range(len(user_genre_list)):
                for b in range(len(new_genre_list)):
                    if new_genre_list[b] == user_genre_list[a]:
                        match_count += 1
                if match_count >= 2:
                    
                    same_genre_list += [new_game["name"]]
                    break
                        
        except (KeyError): 
            x = int(x) + 1
            x = str(x)
            continue
    return same_genre_list
    
####################################################################################################
#JOKES API
def jokes():
    url = "https://v2.jokeapi.dev/joke/Any?type=single"
    params = {"blacklistFlags": "nsfw,racist,sexist,explicit,religious,political"}
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["type"] == "single":
            return(data["joke"])
        else:
            return (data["setup"]), (data["delivery"])
    else:
        return("Error fetching joke:", response.status_code)
    
    
####################################################################################################

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email FROM Users WHERE email = '{0}'".format(email)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def load_user(email):
    users = getUserList()
    if not(email) or email not in str(users):
    	return
    user = User()
    user.id = email
    return user

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    callback_url = url_for('authorized', _external=True)
    return google.authorize(callback=callback_url)

@app.route('/authorized', methods = ['GET', 'POST'])
def authorized():
    if request.method == 'GET':
        resp = google.authorized_response()
        if resp is None:
            return 'Access denied: reason={0} error={1}'.format(
                request.args['error_reason'],
                request.args['error_description']
            )
        access_token = resp['access_token']
        # do something with the access token, e.g. fetch user's email address
        headers = {'Authorization': 'Bearer ' + access_token}
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
        email = r.json().get('email')
        test = isEmailUnique(email)
        if test:
            cursor = conn.cursor() 
            cursor.execute("INSERT INTO Users (email) VALUES (%s)", (email,))
            conn.commit()
        else:
            print("email exisits")
        return render_template('profile.html', username = email)
    else:
        try:
            game_name1 = request.form.get('new')
            joke = jokes()
            #replaced spaces with dashes
            game_name = (replace_space(game_name1))
            game_list = game(game_name)
        except:
            return render_template('profile.html', username = 'jdkim128@bu.edu')
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO User_Games (game_name) VALUES (%s)", (game_name,))
        conn.commit()
        
        game_played = getAllGames()
        insertAllGames(game_list)
        
        return render_template('mylists.html', items=game_list, played=game_played, flip=False)
    
@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return render_template('logout.html')
    
@app.route('/mylist')
def mylist():
    game_list = pullFive()
    game_played = getAllGames()
    return render_template('mylists.html', items=game_list, played=game_played, flip=True)

def pullFive():
    cursor = conn.cursor() 
    emp = []  
    cursor.execute("SELECT rec_game_name FROM recs ORDER BY RAND() LIMIT 5")  
    emp += cursor.fetchall()
    return emp #NOTE return a list of tuples, [(imgdata, pid, caption), ...]

@app.route('/profile')
def prof():
    return render_template('profile.html', username = 'jdkim128@bu.edu')


if __name__ == '__main__':
    app.run(debug=True, port=7000)


          
