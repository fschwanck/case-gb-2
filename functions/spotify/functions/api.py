

import requests
from time import sleep
from typing import Dict


class SpotifyAPI():
    __baseUrl: str = 'https://api.spotify.com/'
    __authenticationUrl: str = 'https://accounts.spotify.com/api/token'
    __session = requests.Session()

    def __init__(self):
        self.__session.headers.update({"Accept" : "application/json"})

    def auth(self, clientId: str, clientSecret: str):
        credentials = { 
                        'grant_type': 'client_credentials',
                        'client_id': clientId,
                        'client_secret': clientSecret
                    }
        token = requests.post(self.__authenticationUrl, credentials, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()
        self.__session.headers.update({"Authorization" : f"{token['token_type']} {token['access_token']}"})
           
    def __getData(self, url: str, params: Dict= None, retries: int=5) -> dict:
        while retries > 0:
            data = None
            response = self.__session.get(url, params=params)
            print(response)
            if response.ok:
                return response.json()
            elif response.status_code == 429:
                sleep(int(response.headers['retry-after']))
                retries -= 1
            else:
                raise Exception(str(response) + ' ' + response.text)
   
    def getSearch(self, 
                  q: str,
                  type: str, 
                  market: str = None, 
                  limit: int = 20, 
                  offset: int = 0, 
                  include_external: str = None, 
                  version: str= 'v1'):
        endpoint = '/search'
        params = {
            'q': q,
            'type': type,
            'market': market,
            'limit': limit,
            'offset': offset,
            'include_external': include_external
        }
        return self.__getData(self.__baseUrl + version + endpoint, params)
    
    def getAllShowEpisodes(self, 
                  id: str,
                  market: str = None,
                  limit: int = 50,
                  version: str= 'v1'):
        endpoint = f'/shows/{id}/episodes'
        params = {
            'id': id,
            'market': market,
            'limit': limit
        }
        episodes = {
            'total' : 0,
            'items': []
            }
        
        data = self.__getData(self.__baseUrl + version + endpoint, params)
        has_next = data['next']
        total = data['total'] + episodes['total']
        episodes.update({'total': total})
        items = episodes['items']
        items.extend(data['items']) 
        episodes.update({'items': items})
        while has_next:
            data = self.__getData(data['next'])
            total = data['total'] + episodes['total']
            episodes.update({'total': total})
            items = episodes['items']
            items.extend(data['items']) 
            episodes.update({'items': items})
            has_next = data['next']
        return episodes
    

    
    def getSeveralEpisodes(self, 
                  ids: str,
                  market: str = None, 
                  version: str= 'v1'):
        endpoint = '/episodes'
        params = {
            'ids': ids,
            'market': market,
        }
        return self.__getData(self.__baseUrl + version + endpoint, params)
    
