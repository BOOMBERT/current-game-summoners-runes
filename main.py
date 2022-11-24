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

    def __init__(self, summoner_info_from_request):
        self.summoner_info_from_request = summoner_info_from_request

    def summoner_info(self):
        if check_for_errors(self.summoner_info_from_request):
            return self.summoner_info_from_request.json()

        print("Summoner with this username does not exist")
        sys.exit(1)


class Game:

    def __init__(self, game_info_from_request):
        self.game_info_from_request = game_info_from_request

    def current_game_info(self):
        if check_for_errors(self.game_info_from_request):
            return self.game_info_from_request.json()

        print('The summoner is not currently in the game')
        sys.exit(1)


def get_info_from_request(api_info, api_key, info_to_request):
    return requests.get(
        url=f"{info_to_request}{api_info}",
        params={
            "api_key": api_key
        })

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

def game_summoners_info(current_game_info: dict) -> list[tuple[any, any, any]]:
    summoner_names = (element['summonerName'] for element in current_game_info['participants'])
    champions = (element['championId'] for element in current_game_info['participants'])
    runes = (element['perks']['perkIds'] for element in current_game_info['participants'])

    return list(zip(summoner_names, champions, runes))

def check_player(summoner_name):
    API_KEY = get_api_key()

    summoner_info = get_info_from_request(
        summoner_name,
        API_KEY,
        API_ENDPOINTS["get_summoner_info"]
    )

    summoner = Summoner(summoner_info)

    current_game_info = get_info_from_request(
        summoner.summoner_info()['id'],
        API_KEY,
        API_ENDPOINTS["get_current_game_info"],
    )

    current_game = Game(current_game_info)

    game_info = current_game.current_game_info()
    print(game_summoners_info(game_info))


if __name__ == "__main__":
    check_player("Qwertyyy3")
