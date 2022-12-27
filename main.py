from os import getenv
from dotenv import load_dotenv
import requests
from references import API_ENDPOINTS, GAME_DATA
import operations_on_data


def get_summoner_info(summoner_info_endpoint, summoner_name, api_key) -> dict | None:
    summoner_info_from_request = get_info_from_request(
        summoner_info_endpoint, summoner_name, api_key
    )

    if check_summoner_info_request := check_for_errors(summoner_info_from_request):
        return summoner_info_from_request.json()

    elif not check_summoner_info_request:
        print("Summoner with this username does not exist")

    return None


def get_current_game_info(current_game_info_endpoint, summoner_id, api_key) -> dict | None:
    game_info_from_request = get_info_from_request(
        current_game_info_endpoint, summoner_id, api_key
    )

    if check_current_game_request := check_for_errors(game_info_from_request):
        return game_info_from_request.json()

    elif not check_current_game_request:
        print("The summoner is not currently in the game")

    return None


def check_for_errors(request: requests.Response) -> bool | None:
    if request.ok:
        return True

    try:
        request.raise_for_status()

    except requests.exceptions.RequestException as request_error:
        NO_ACCESS_CODE = 404
        current_error_code = request_error.response.status_code

        if current_error_code == NO_ACCESS_CODE:
            return False

        print(
            f"Error code: {current_error_code}\n"
            f"Error message: {request_error.response.reason}"
        )
        return None


def get_info_from_request(
    api_info: str,
    info_to_request: str,
    api_key: str,
) -> requests.Response:
    return requests.get(url=f"{api_info}{info_to_request}", params={"api_key": api_key})


def changed_current_game_summoners_info(
    isolated_summoners_info: list[tuple[any, any, any]],
    url_to_champions_data: str,
    url_to_runes_data: str,
) -> dict[str, dict[str, tuple[str]]]:
    final_summoners_info = {}

    for summoner in isolated_summoners_info:
        summoner_name = summoner[0]
        champion_id = summoner[1]
        rune_ids = summoner[2]

        final_summoners_info[summoner_name] = {
            "champion_name": operations_on_data.change_champion_id_to_champion_name(
                champion_id, url_to_champions_data
            ),
            "rune_names": operations_on_data.change_player_rune_ids_to_rune_names(
                rune_ids, url_to_runes_data
            ),
        }

    return final_summoners_info


def check_the_player_current_game(summoner_name: str) -> dict[str, dict[str, tuple[str]]] | None:
    summoner_info = get_summoner_info(
        API_ENDPOINTS["get_summoner_info"], summoner_name, getenv("API_KEY")
    )

    if summoner_info is None:
        return None

    current_game_info = get_current_game_info(
        API_ENDPOINTS["get_current_game_info"], summoner_info["id"], getenv("API_KEY")
    )

    if current_game_info is None:
        return None

    isolated_summoners_info = operations_on_data.isolate_needed_summoners_info(current_game_info)
    url_to_champions_data = GAME_DATA["get_champions_data"]
    url_to_runes_data = GAME_DATA["get_runes_data"]

    return changed_current_game_summoners_info(
        isolated_summoners_info, url_to_champions_data, url_to_runes_data
    )


if __name__ == "__main__":
    load_dotenv()
    name_of_the_summoner = input("Enter the summoner's name -> ")
    print(check_the_player_current_game(name_of_the_summoner))
