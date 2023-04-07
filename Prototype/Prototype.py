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
app = Flask(__name__)

#api key for rawg: 2f70e298b9ba477e80cc87048455f30a

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
        return render_template('display.html', description = descrip)
    else:
        return render_template('search.html')
        
if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python game-rank-backend.py
	app.run(port = 8888, debug=True)
