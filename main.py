from typing import Dict, List, Tuple, Any
from os import getenv
import json
from dotenv import load_dotenv
import requests
from references import API_ENDPOINTS, GAME_DATA
import operations_on_data


def get_checked_info(
        api_info: str,
        info_to_request: str,
        api_key: str,
        error_message: str
) -> Dict[Any, Any] | None:
    info_from_request = get_info_from_request(
        api_info, info_to_request, api_key
    )

    if check_the_request_for_error(info_from_request, error_message):
        return info_from_request.json()

    return None


def get_info_from_request(
    api_info: str,
    info_to_request: str,
    api_key: str
) -> requests.Response:
    return requests.get(url=f"{api_info}{info_to_request}", params={"api_key": api_key})


def check_the_request_for_error(request: requests.Response, error_message: str) -> bool:
    try:
        request.raise_for_status()

        return True

    except requests.exceptions.RequestException as request_error:
        NO_ACCESS_CODE = 404
        current_error_code = request_error.response.status_code

        if current_error_code == NO_ACCESS_CODE:
            print(error_message)

        else:
            print(
                f"Error code: {current_error_code}\n"
                f"Error message: {request_error.response.reason}"
            )

    return False


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

    return json.dumps(summoners_info, indent=4)


def check_the_summoner_current_game(summoner_name: str, region: str) -> str | None:
    SUMMONER_ERROR_MESSAGE = "Summoner with this username does not exist"
    summoner_api_info = API_ENDPOINTS["get_summoner_info"].replace(" ", region)

    summoner_info = get_checked_info(
        api_info=summoner_api_info,
        info_to_request=summoner_name,
        api_key=getenv("API_KEY"),
        error_message=SUMMONER_ERROR_MESSAGE
    )

    if summoner_info is None:
        return None

    CURRENT_GAME_ERROR_MESSAGE = "The summoner is not currently in the game"
    current_game_api_info = API_ENDPOINTS["get_current_game_info"].replace(" ", region)
    summoner_id = summoner_info["id"]

    current_game_info = get_checked_info(
        api_info=current_game_api_info,
        info_to_request=summoner_id,
        api_key=getenv("API_KEY"),
        error_message=CURRENT_GAME_ERROR_MESSAGE
    )

    if current_game_info is None:
        return None

    isolated_summoners_info = operations_on_data.isolate_needed_summoners_info(current_game_info)
    return needed_current_game_summoners_info(
        isolated_summoners_info=isolated_summoners_info,
        url_to_champions_data=GAME_DATA["get_champions_data"],
        url_to_runes_data=GAME_DATA["get_runes_data"]
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
