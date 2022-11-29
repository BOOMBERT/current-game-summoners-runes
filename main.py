import sys
import requests


API_ENDPOINTS = {
    "get_summoner_info": "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/",
    "get_current_game_info": "https://eun1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/",
}

DATAS = {
    "get_champions_data": "https://raw.communitydragon.org/"
    "latest/plugins/rcp-be-lol-game-data/global/default/v1/champions/",
    "get_runes_data": "https://raw.communitydragon.org/"
    "latest/plugins/rcp-be-lol-game-data/global/default/v1/perks.json",
}


class Summoner:
    def __init__(self, summoner_info_from_request: requests.Response):
        self._summoner_info_from_request = summoner_info_from_request

    def summoner_info(self) -> dict | None:
        if check_for_errors(self._summoner_info_from_request):
            return self._summoner_info_from_request.json()

        print("Summoner with this username does not exist")
        return None


class Game:
    def __init__(self, game_info_from_request: requests.Response):
        self._game_info_from_request = game_info_from_request

    def current_game_info(self) -> dict | None:
        if check_for_errors(self._game_info_from_request):
            return self._game_info_from_request.json()

        print("The summoner is not currently in the game")
        return None


def check_for_errors(request: requests.Response) -> bool:
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


def get_info_from_request(api_info: str, info_to_request: str, api_key: str) -> requests.Response:
    return requests.get(url=f"{api_info}{info_to_request}", params={"api_key": api_key})


def get_api_key() -> str:
    with open("my_api_key.txt", "r", encoding="utf-8") as file_with_api_key:
        return file_with_api_key.read()


def isolation_the_summoners_game_info(current_game_info: dict) -> list[tuple[any, any, any]]:
    summoner_names = (element["summonerName"] for element in current_game_info["participants"])
    champions = (element["championId"] for element in current_game_info["participants"])
    runes = (element["perks"]["perkIds"] for element in current_game_info["participants"])

    return list(zip(summoner_names, champions, runes))


def changing_champion_id_to_name(champion_id: str, url_to_data: str) -> str:
    url_data = f"{url_to_data}{champion_id}.json"
    return requests.get(url_data).json()["name"]


def changing_player_rune_ids_to_names(rune_ids: list[int], url_to_data: str) -> tuple[str]:
    data = requests.get(url_to_data).json()
    return tuple(''.join((section["name"] for section in data if section["id"] == rune_id)) for rune_id in rune_ids)


def check_player_current_game(summoner_name: str):
    api_key = get_api_key()

    summoner_info_from_request = get_info_from_request(
        API_ENDPOINTS["get_summoner_info"], summoner_name, api_key
    )

    summoner = Summoner(summoner_info_from_request)
    summoner_info = summoner.summoner_info()

    if summoner_info is None:
        return None

    current_game_info = get_info_from_request(
        API_ENDPOINTS["get_current_game_info"], summoner_info["id"], api_key
    )

    current_game = Game(current_game_info)
    game_info = current_game.current_game_info()

    return None if game_info is None else isolation_the_summoners_game_info(game_info)


if __name__ == "__main__":
    print(check_player_current_game(""))
    # print(changing_player_rune_ids_to_names(
    #     [8128, 8139, 8138, 8106, 8313, 8321, 5008, 5008, 5002], DATAS["get_runes_data"])
    # )
