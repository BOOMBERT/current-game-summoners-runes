import sys
import requests


with open("api_key", "r", encoding="utf-8") as file:
    API_KEY = file.read()

API_ENDPOINTS = {
    "get_summoner_info":
        'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/',
    "get_current_game_info":
        'https://eun1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'
}


class Summoner:

    def __init__(self, summoner_name, summoner_info_api, current_game_info_api, api_key):
        self.summoner_name = summoner_name
        self.summoner_info_api = summoner_info_api
        self.current_game_info_api = current_game_info_api
        self._api_key = api_key
        self._summoner_id = None
        self.no_access_code = 404
        self._current_game_info = None
        self._get_summoner_info()
        self._get_current_game_info()

    def _get_summoner_info(self):
        summoner_info_request = requests.get(
            url=f"{self.summoner_info_api}{self.summoner_name}",
            params={
                "api_key": self._api_key
            })

        if summoner_info_request.status_code == self.no_access_code:
            print("Summoner with this username does not exist")
            sys.exit(1)

        elif not check_for_errors(summoner_info_request):
            _summoner_info = summoner_info_request.json()
            self._summoner_id = _summoner_info["id"]

            return _summoner_info

        return None

    def _get_current_game_info(self):
        current_game_info_request = requests.get(
            url=f"{self.current_game_info_api}{self._summoner_id}",
            params={
                "api_key": self._api_key
            })

        if current_game_info_request.status_code == self.no_access_code:
            print('The summoner is not currently in the game')
            sys.exit(1)

        elif not check_for_errors(current_game_info_request):
            self._current_game_info = current_game_info_request.json()

            return self._current_game_info

        return None

    def current_game_summoners_info(self):
        summoner_names = []
        champions = []
        runes = []

        for participant in self._current_game_info['participants']:
            summoner_names.append(participant['summonerName'])
            champions.append(participant['championId'])
            runes.append(participant['perks']['perkIds'])

        zipped_data = list(zip(summoner_names, champions, runes))

        return zipped_data


def check_for_errors(request):
    if not request.ok:
        try:
            request.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"Request Error: {error}")
            sys.exit(1)

    return False

def display_current_game_info(current_game_info):
    print(current_game_info)

def check_player(username):
    summoner = Summoner(
        username,
        API_ENDPOINTS["get_summoner_info"],
        API_ENDPOINTS["get_current_game_info"],
        API_KEY)

    current_game_info = summoner.current_game_summoners_info()
    display_current_game_info(current_game_info)


if __name__ == "__main__":
    check_player("")
