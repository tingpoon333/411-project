#code to get the platforms of the game
#['Android', 'PS Vita', 'PlayStation 4', 'PlayStation 3', 'Xbox 360', 'Nintendo 3DS', 'Nintendo Switch', 'macOS', 'PC', 'iOS', 'Wii U', 'Xbox One', 'Linux']
descrip = y["platforms"] 
new = []
for i in range(len(descrip)):
    new += [descrip[i]['platform']['name']]
    
#code for developers of the game
descrip = y['developers']
new = []
for i in range(len(descrip)):
    new += [descrip[i]['name']]
    
#code to get the genres of a game
descrip = y["genres"]
genres = []
for i in range(len(descrip)):
    genres += [descrip[i]['name']]
