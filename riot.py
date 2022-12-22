from types import NoneType
import requests
import time

class Riot:
    """
        ### Parameters
        - api_key : str
            Your api key
        - ratelimit : float
            The time between each request in seconds
        
        ### Example
        ```python
        >>> from riot import Riot , Player , Clash
        >>> riot=Riot(api_key="RGAPI-07xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",ratelimit=1.2)
        >>> player=Player(riot=riot,pseudo="Toms34")
        >>> clash=Clash(riot=riot)
        >>> print(player.get_match())
        ```
    """
    def __init__(self,api_key : str ,ratelimit : float =1.2) -> None:
        """
        ### Parameters
        - api_key : str
            Your api key
        - ratelimit : float
            The time between each request in seconds
        
        ### Example
        ```python
        >>> from riot import Riot , Player , Clash
        >>> riot=Riot(api_key="RGAPI-07xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        >>> player=Player(riot=riot,pseudo="Toms34")
        >>> clash=Clash(riot=riot)
        >>> print(player.get_match())
        ```
        """
        self.api_key=api_key
        self.headers = {
            "X-Riot-Token": self.api_key
        }
        self.last_request=0
        self.rate_limit=ratelimit
    
    def requested(self):
        self.last_request=time.time()
    
    def can_request(self):
        if time.time()-self.last_request>1.2:
            return
        time.sleep(self.rate_limit -(time.time()-self.last_request))
        self.requested()
        
    def get_summoner_by_name(self,pseudo):
        url_id=f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"

        #request
        self.can_request()
        resp = requests.get(url=url_id, headers=self.headers)
        self.requested()
        data = resp.json()

        #Encrypted PUUID. 78 char
        #print(data.keys())
        #print(data)
        if resp.status_code == 404:
            return "404"
        return data

    def get_puuid(self,pseudo)-> None:
        #url to request summoner puuid (encrypted) just ad user name after
        url_id=f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"

        #request
        self.can_request()
        resp = requests.get(url=url_id, headers=self.headers)
        self.requested()
        data = resp.json()

        #Encrypted PUUID. 78 char
        #print(data.keys())
        #print(data)
        if resp.status_code == 404:
            return NoneType
        return data["puuid"]

    def get_encrypted_id(self,pseudo)-> str:
        #url to request summoner puuid (encrypted) just ad user name after
        url_id=f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pseudo}"

        #request
        self.can_request()
        resp = requests.get(url=url_id, headers=self.headers)
        self.requested()
        data = resp.json()

        #Encrypted PUUID. 78 char
        #print(data.keys())
        #print(data)
        if resp.status_code == 404:
            return "404"
        # print(data["id"])
        return data["id"]

class Player:
    
        def __init__(self,riot,pseudo) -> None:
            self.riot=riot
            self.encryptedId=riot.get_encrypted_id(pseudo=pseudo)
            self.puuid=riot.get_puuid(pseudo=pseudo)
            self.gameMode={
                "aram":450,
                "flex":440,
                "blind":430,
                "solo":420,
                "normal":400
            }

        def get_match(self,GameMode,start=0,count=100):
            #queue flex = 440
            if GameMode not in self.gameMode:
                url_match_id=f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start={start}&count={count}"
            else:
                url_match_id=f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?queue={self.gameMode[GameMode]}&start={start}&count={count}" #?queue=440&start={start}&count={count}"

            self.riot.can_request()
            resp=requests.get(url=url_match_id,headers=self.riot.headers)
            self.riot.requested()
            match_id=resp.json()
            if resp.status_code != 200:
                return resp.status_code
            return match_id

        def get_match_by_id(self,match_id):
            url_match_by_id=f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
            self.riot.can_request()
            resp=requests.get(url=url_match_by_id,headers=self.riot.headers)
            self.riot.requested()
            data= resp.json()
            if resp.status_code != 200:
                return resp.status_code
            return data
        
        def get_all_masteries(self):
            url_masteries=f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.encryptedId}"
            self.riot.can_request()
            resp=requests.get(url=url_masteries,headers=self.riot.headers)
            self.riot.requested()
            data= resp.json()
            if resp.status_code != 200:
                return resp.status_code
            return data

        def get_mastery_by_champion(self,champion_id):
            url_masteries=f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.encryptedId}/by-champion/{champion_id}"
            self.riot.can_request()
            resp=requests.get(url=url_masteries,headers=self.riot.headers)
            self.riot.requested()
            data= resp.json()
            if resp.status_code != 200:
                return resp.status_code
            return data
        
class Clash:
    def __init__(self,riot) -> None:
        self.riot=riot

    def get_clash_by_summoner(self,player:Player):
        encryptedId=player.encryptedId
        url_clash=f"https://euw1.api.riotgames.com/lol/clash/v1/players/by-summoner/{encryptedId}"
        self.riot.can_request()
        resp=requests.get(url=url_clash,headers=self.riot.headers)
        self.riot.requested()
        data= resp.json()
        if resp.status_code != 200:
            return resp.status_code
        return data

    def get_clash_by_team(self,teamId):
        url_clash=f"https://euw1.api.riotgames.com/lol/clash/v1/teams/{teamId}"
        self.riot.can_request()
        resp=requests.get(url=url_clash,headers=self.riot.headers)
        self.riot.requested()
        data= resp.json()
        if resp.status_code != 200:
            return resp.status_code
        return data

    def get_clash_by_tournament(self,tournamentId):
        url_clash=f"https://euw1.api.riotgames.com/lol/clash/v1/tournaments/{tournamentId}"
        self.riot.can_request()
        resp=requests.get(url=url_clash,headers=self.riot.headers)
        self.riot.requested()
        data= resp.json()
        if resp.status_code != 200:
            return resp.status_code
        return data

    def get_clash_by_tournament_team(self,teamId):
        url_clash=f"https://euw1.api.riotgames.com/lol/clash/v1/tournaments/by-team/{teamId}"
        self.riot.can_request()
        resp=requests.get(url=url_clash,headers=self.riot.headers)
        self.riot.requested()
        data= resp.json()
        if resp.status_code != 200:
            return resp.status_code
        return data

