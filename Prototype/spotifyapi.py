"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# Set up Spotify API credentials
redirect_uri = 'http://localhost:7000/callback'
client_id = 'd8c356355725447eba3fceab71d032a0'
client_secret = '9d16c781b9b14ae0a81e83b334654ad9'

# Set up authentication
scope = 'user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Search for the song you want to play on a loop
results = sp.search(q='Objects in the Mirror Mac Miller', type='track', limit=1)
uri = results['tracks']['items'][0]['uri']

# Start playing the song on a loop
while True:
    sp.start_playback(uris=[uri])
    time.sleep(100) # adjust the sleep time to change the loop duration
"""
"""
from flask import Flask, render_template, request, redirect, session
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time
import os

app = Flask(__name__)

# Set up Spotify API credentials
os.environ['SPOTIPY_CLIENT_ID'] = 'd8c356355725447eba3fceab71d032a0'
os.environ['SPOTIPY_CLIENT_SECRET'] = '9d16c781b9b14ae0a81e83b334654ad9'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:7000/callback'

# Set up authentication
scope = 'user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/play', methods=['POST'])
def play():
    song = request.form['song'] # get the song input from the form
    results = sp.search(q=song, type='track', limit=1) # search for the song
    uri = results['tracks']['items'][0]['uri'] # get the song URI

    # Start playing the song on a loop
    while True:
        sp.start_playback(uris=[uri])
        time.sleep(5) # adjust the sleep time to change the loop duration
"""
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask
import time

# Set up Spotify API credentials
redirect_uri = 'http://localhost:7000/callback'
client_id = 'd8c356355725447eba3fceab71d032a0'
client_secret = '9d16c781b9b14ae0a81e83b334654ad9'

# Set up authentication
scope = 'user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Search for the song you want to play on a loop
results = sp.search(q='Objects in the Mirror Mac Miller', type='track', limit=1)
uri = results['tracks']['items'][0]['uri']

# Create a Flask app
app = Flask(__name__)

# Define a route to start the loop
@app.route('/start_loop')
def start_loop():
    # Start playing the song on a loop
    while True:
        sp.start_playback(uris=[uri])
        time.sleep(5) # adjust the sleep time to change the loop duration
        
# Run the app
if __name__ == '__main__':
    app.run()
"""
"""
from flask import Flask
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

# Start playing the song on a loop
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

if __name__ == '__main__':
    app.run(port= 7000, debug=True)
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify API credentials
redirect_uri = 'http://localhost:7000/callback'
client_id = 'd8c356355725447eba3fceab71d032a0'
client_secret = '9d16c781b9b14ae0a81e83b334654ad9'

# Set up authentication
scope = 'user-modify-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Get access token
access_token = sp.auth_manager.get_access_token(as_dict=False)
print(access_token)


import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up Spotify API credentials
redirect_uri = 'http://localhost:7000'
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

# Set up authentication
scope = 'user-modify-playback-state user-read-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# Search for the song you want to play on a loop
results = sp.search(q='Gaming Lofi', type='track', limit=1)
uri = results['tracks']['items'][0]['uri']

print(uri) # prints the URI of the first search result
