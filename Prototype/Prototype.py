#code setup for connecting with database (MySql)
"""
import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'Group_8_Project'

#change based on the mysql database we are using
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''
mysql.init_app(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()
"""
import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
import requests
from requests import post
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

app = Flask(__name__)

# Set up Spotify API credentials
redirect_uri = 'http://127.0.0.1:7000/callback'
client_id = 'd8c356355725447eba3fceab71d032a0'
client_secret = '9d16c781b9b14ae0a81e83b334654ad9'

# Set up authentication
scope = 'user-modify-playback-state user-read-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Search for the song you want to play on a loop
results = sp.search(q='Gaming Lofi', type='track', limit=1)
uri = results['tracks']['items'][0]['uri']


#api key for rawg: 2f70e298b9ba477e80cc87048455f30a

@app.before_first_request
def play_on_loop():
    while True:
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']
            # Play the song on the specified device
            sp.start_playback(device_id=device_id, uris=[uri], context_uri=None, offset=None)
            print('Playing "Objects in the Mirror" on device ID:', device_id)
            break
        #sp.start_playback(uris=[uri])
        #time.sleep(5) # adjust the sleep time to change the loop duration
        else:
            print('No devices found. Trying again in 5 seconds...')
            time.sleep(5)
            
@app.route("/", methods=['GET', 'POST'])
def search_game_by_name():
    if request.method == 'POST':
        name = request.form.get('game_name')
        url = "https://rawg-video-games-database.p.rapidapi.com/games/" + name + "?key=2f70e298b9ba477e80cc87048455f30a"

        headers = {
        	"X-RapidAPI-Key": "7740c2a325msh0911c68659b1739p1f47f3jsn641fd99e2bf0",
        	"X-RapidAPI-Host": "rawg-video-games-database.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)
        y = json.loads(response.text)
        descrip = y["description"]
        return render_template('display2.html', description = descrip)
    else:
        return render_template('search.html')
        
if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python game-rank-backend.py
	app.run(port = 8888, debug=True)
