from riot import Riot , Player , Clash
import time

def get_oldest_game(player : Player ,gamemode=None):
    game = player.get_match(gamemode)
    i=0
    while len(game) == 100:
        i+=100
        game = player.get_match(gamemode,start=i)
    print(i+len(game))
    return game[-1]

def gameid_to_datetime(player : Player,game_id):
    game_data = player.get_match_by_id(game_id)
    game_start = game_data["info"]["gameStartTimestamp"]
    return time.gmtime(game_start/1000)

def get_best_data(player : Player ,gamemode=None):
    game = player.get_match(None)
    i=0
    while len(game) == 100:
        i+=100
        game = player.get_match(None,start=i)
    print(i+len(game))
    return game[-1]