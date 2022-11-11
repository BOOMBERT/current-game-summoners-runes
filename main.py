import sys
import requests


API_ENDPOINTS = {
    "get_summoner_info":
        'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/',
    "get_current_game_info":
        'https://eun1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'
}

DATAS = {
    "get_champions_data":
        "https://raw.communitydragon.org/"
        "latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/",
    "get_runes_data":
        "https://raw.communitydragon.org/"
        "latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json",
}

def get_api_key():
    with open("api_key", "r", encoding="utf-8") as file:
        return file.read()


class Summoner:

    def __init__(self, summoner_name, summoner_info_api, api_key):
        self._summoner_name = summoner_name
        self._summoner_info_api = summoner_info_api
        self._api_key = api_key
        self._summoner_info = None

    def get_summoner_info(self):
        summoner_info_request = requests.get(
            url=f"{self._summoner_info_api}{self._summoner_name}",
            params={
                "api_key": self._api_key
            })

        if check_for_errors(summoner_info_request):
            self._summoner_info = summoner_info_request.json()

            return self._summoner_info

        print("Summoner with this username does not exist")
        sys.exit(1)


class Game:

    def __init__(self, current_game_info_api, api_key, game_info):
        self._current_game_info_api = current_game_info_api
        self._api_key = api_key
        self._game_info = game_info
        self._current_game_info = None

    def get_current_game_info(self):
        current_game_info_request = requests.get(
            url=f"{self._current_game_info_api}{self._game_info['id']}",
            params={
                "api_key": self._api_key
            })

        if check_for_errors(current_game_info_request):
            self._current_game_info = current_game_info_request.json()

            return self._current_game_info

        print('The summoner is not currently in the game')
        sys.exit(1)


def current_game_summoners_info(current_game_info):
    summoner_names = []
    champions = []
    runes = []

    for participant in current_game_info['participants']:
        summoner_names.append(participant['summonerName'])
        champions.append(participant['championId'])
        runes.append(participant['perks']['perkIds'])

    return list(zip(summoner_names, champions, runes))

def check_for_errors(request):
    if request.ok:
        return True

    try:
        request.raise_for_status()
    except requests.exceptions.RequestException as request_error:
        NO_ACCESS_CODE = "404"
        current_error_code = str(request_error)[:3]

        if current_error_code == NO_ACCESS_CODE:
            return False

        print(f"Request Error: {request_error}")
        sys.exit(1)

def replace_ids_into_names():
    pass

def check_player(summoner_name):
    API_KEY = get_api_key()

    summoner = Summoner(
        summoner_name,
        API_ENDPOINTS["get_summoner_info"],
        API_KEY
    )

    game = Game(
        API_ENDPOINTS["get_current_game_info"],
        API_KEY,
        summoner.get_summoner_info()
    )

    current_game_info = game.get_current_game_info()
    print(current_game_summoners_info(current_game_info))


if __name__ == "__main__":
    check_player("")
