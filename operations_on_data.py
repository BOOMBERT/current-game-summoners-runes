from typing import List
import requests

from references import GAME_DATA
from request_operations import check_the_request_for_error


def change_champion_id_to_champion_name(champion_id: int) -> str | None:
    URL_TO_CHAMPION_DATA = GAME_DATA["get_champions_data"]
    champion_data = f"{URL_TO_CHAMPION_DATA}{champion_id}.json"
    champion_info_from_data = requests.get(champion_data)

    if check_the_request_for_error(champion_info_from_data):
        return champion_info_from_data.json()["name"]

    return None


def change_player_runes_ids_to_runes_names(runes_ids: List[int]) -> List[str] | None:
    URL_TO_RUNES_DATA = GAME_DATA["get_runes_data"]
    runes_data = requests.get(URL_TO_RUNES_DATA)

    if check_the_request_for_error(runes_data):
        runes_data = runes_data.json()
        runes_names = [""] * len(runes_ids)
        counter = 0

        for rune in runes_data:
            if runes_ids.count(rune["id"]) == 2:
                runes_names[runes_ids.index(
                    rune["id"], runes_ids.index(rune["id"]) + 1, len(runes_data)
                )] = rune["name"]
                counter += 1

            if rune["id"] in runes_ids:
                runes_names[runes_ids.index(rune["id"])] = rune["name"]
                counter += 1

            if counter == len(runes_ids):
                break

        return runes_names

    return None
