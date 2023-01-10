from typing import Dict, List, Tuple, Any
from os import getenv
import json
import requests
from dotenv import load_dotenv

import references
import operations_on_data
import request_functions


class Summoner:
    SUMMONER_ERROR_MESSAGE = "Summoner with this username does not exist"

    def __init__(self) -> None:
        self._summoner_info = None

    def assign_checked_summoner_info(
            self, summoner_info_request: requests.Response
    ) -> bool:
        if request_functions.check_the_request_for_error(
                summoner_info_request,
                self.SUMMONER_ERROR_MESSAGE
        ):
            self._summoner_info = summoner_info_request.json()
            return True

        return False

    def id(self) -> str | None:
        try:
            return self._summoner_info["id"]

        except KeyError:
            print("ID not found")
            return None


class CurrentGame:
    CURRENT_GAME_ERROR_MESSAGE = "The summoner is not currently in the game"

    def __init__(self) -> None:
        self._current_game_info = None

    def assign_checked_current_game_info(
            self, current_game_info_request: requests.Response
    ) -> bool:
        if request_functions.check_the_request_for_error(
                current_game_info_request,
                self.CURRENT_GAME_ERROR_MESSAGE
        ):
            self._current_game_info = current_game_info_request.json()
            return True

        return False

    def info(self) -> Dict[Any, Any] | None:
        if self._current_game_info is not None:
            return self._current_game_info

        print("Current game info not found")
        return None


def needed_current_game_summoners_info(
        isolated_summoners_info: List[Tuple[str, int, List[int]]],
        url_to_champions_data: str,
        url_to_runes_data: str
) -> str:
    summoners_info = {}

    for summoner in isolated_summoners_info:
        summoner_name = summoner[0]
        champion_id = summoner[1]
        rune_ids = summoner[2]

        summoners_info[summoner_name] = {
            "champion_name": operations_on_data.change_champion_id_to_champion_name(
                champion_id, url_to_champions_data
            ),
            "rune_names": operations_on_data.change_player_rune_ids_to_rune_names(
                rune_ids, url_to_runes_data
            )
        }

    return json.dumps(summoners_info, indent=4, ensure_ascii=False)


def check_the_summoner_current_game(summoner_name: str, region: str) -> str | None:
    summoner_api_url = references.API_ENDPOINTS["get_summoner_info"].replace(" ", region)
    current_game_api_url = references.API_ENDPOINTS["get_current_game_info"].replace(" ", region)

    summoner_info_request = request_functions.get_info_from_request(
        api_info=summoner_api_url, info_to_request=summoner_name, api_key=getenv("API_KEY")
    )

    summoner = Summoner()
    if not summoner.assign_checked_summoner_info(summoner_info_request):
        return None

    current_game_info_request = request_functions.get_info_from_request(
        api_info=current_game_api_url, info_to_request=summoner.id(), api_key=getenv("API_KEY")
    )

    current_game = CurrentGame()
    if not current_game.assign_checked_current_game_info(current_game_info_request):
        return None

    current_game_info = current_game.info()
    isolated_summoners_info = operations_on_data.isolate_needed_summoners_info(current_game_info)

    return needed_current_game_summoners_info(
        isolated_summoners_info=isolated_summoners_info,
        url_to_champions_data=references.GAME_DATA["get_champions_data"],
        url_to_runes_data=references.GAME_DATA["get_runes_data"]
    )


if __name__ == "__main__":
    load_dotenv()
    REGIONS = ("BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1", "RU", "TR1")
    region_name = input(f"{', '.join(REGIONS)}\nEnter the region name -> ")

    if region_name.upper() in REGIONS:
        name_of_the_summoner = input("Enter the summoner's name -> ")
        print(check_the_summoner_current_game(name_of_the_summoner, region_name.lower()))

    else:
        print("Unknown region")
        