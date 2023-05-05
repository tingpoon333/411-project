# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login
import requests
from requests import post
import json

#game id cap number #949995
name = "elden-ring"
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
while len(same_genre_list) < 5:
    try:
        counter += 1
        x = str(user_game_id + counter)
        url = "https://rawg-video-games-database.p.rapidapi.com/games/" + x + "?key=2f70e298b9ba477e80cc87048455f30a"
        new_response = requests.request("GET", url, headers=headers)
        new_game = json.loads(new_response.text)
        #print(new_game)
        #print(new_game['name'])
        
        #outputs the genre list of the iterated game
        new_game_genres = new_game["genres"]
        new_game_id = new_game['id']
        #print(new_game_genres)
        #print(new_game)
        new_genre_list = []
        for i in range(len(new_game_genres)):
            new_genre_list += [new_game_genres[i]['name']]
            
        #print(user_genre_list)    
        #print(new_genre_list)

        match_count = 0
        for a in range(len(user_genre_list)):
            for b in range(len(new_genre_list)):
                if new_genre_list[b] == user_genre_list[a]:
                    match_count += 1
            if match_count >= 2:
                same_genre_list += [new_game["name"]]
                break
        
        for i in range(len(same_genre_list)):
            print(same_genre_list[0])
            print(same_genre_list[0]["metacritic"])
            print(type(same_genre_list[0]["metacritic"]))
            if int(same_genre_list[i]["metacritic"]) <= int(same_genre_list[i + 1]["metacritic"]) :
                x = same_genre_list[i]["name"]
                same_genre_list[i] = same_genre_list[i + 1]['name']
                same_genre_list[i + 1] = x
                
                    
    except (KeyError): 
        x = int(x) + 1
        x = str(x)
        continue
#print(user_genre_list)
#print(new_genre_list)
print(same_genre_list)