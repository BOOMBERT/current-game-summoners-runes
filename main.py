import sys
import requests
from os import getenv
from dotenv import load_dotenv
from references import API_ENDPOINTS, GAME_DATA
from operations_on_data import (
    isolation_the_summoners_info,
    changing_champion_id_to_name,
    changing_player_rune_ids_to_names,
)


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


def get_info_from_request(
    api_info: str, info_to_request: str, api_key: str
) -> requests.Response:
    return requests.get(url=f"{api_info}{info_to_request}", params={"api_key": api_key})


def get_changed_summoner_info_in_dict(
    champion_id: str,
    rune_ids: list[int],
    url_to_champions_data: str,
    url_to_runes_data: str,
) -> dict[str, tuple[str]]:
    return {
        "champion_name": changing_champion_id_to_name(champion_id, url_to_champions_data),
        "rune_names": changing_player_rune_ids_to_names(rune_ids, url_to_runes_data),
    }


def dict_with_every_summoner_changed_info(
    isolated_summoners_info: list[tuple[any, any, any]],
    url_to_champions_data: str,
    url_to_runes_data: str,
) -> dict[str, dict[str, tuple[str]]]:
    final_summoners_info = {}

    for summoner in isolated_summoners_info:
        summoner_name = summoner[0]
        champion_id = summoner[1]
        rune_ids = summoner[2]

        final_summoners_info[summoner_name] = get_changed_summoner_info_in_dict(
            champion_id, rune_ids, url_to_champions_data, url_to_runes_data
        )

    return final_summoners_info


def check_the_player_current_game(summoner_name: str) -> dict[str, dict[str, tuple[str]]] | None:
    summoner_info_from_request = get_info_from_request(
        API_ENDPOINTS["get_summoner_info"], summoner_name, getenv("API_KEY")
    )

    summoner = Summoner(summoner_info_from_request)
    summoner_info = summoner.summoner_info()

    if summoner_info is None:
        return None

    current_game_info = get_info_from_request(
        API_ENDPOINTS["get_current_game_info"], summoner_info["id"], getenv("API_KEY")
    )

    current_game = Game(current_game_info)
    game_info = current_game.current_game_info()

    if game_info is None:
        return None

    isolated_summoners_info = isolation_the_summoners_info(game_info)
    url_to_champions_data = GAME_DATA["get_champions_data"]
    url_to_runes_data = GAME_DATA["get_runes_data"]
    return dict_with_every_summoner_changed_info(
        isolated_summoners_info, url_to_champions_data, url_to_runes_data
    )


if __name__ == "__main__":
    load_dotenv()
    print(check_the_player_current_game(""))
