

if __name__=="__main__":
    
    from dotenv import load_dotenv
    from os import getenv
    from riot import Riot , Player , Clash
    from function import get_oldest_game , gameid_to_datetime

    load_dotenv()
    api_key=getenv("API_KEY")
    # Init riot api
    riot=Riot(api_key=api_key)
    player=Player(riot=riot,pseudo="madajel")
    clash=Clash(riot=riot)

    oldest_game=get_oldest_game(player,gamemode="aram")
    print(oldest_game)
    print(gameid_to_datetime(player,oldest_game))
    