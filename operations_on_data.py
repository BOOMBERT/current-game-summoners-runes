import requests


def isolate_needed_summoners_info(current_game_info: dict) -> list[tuple[any, any, any]]:
    summoner_names = (element["summonerName"] for element in current_game_info["participants"])
    champions = (element["championId"] for element in current_game_info["participants"])
    runes = (element["perks"]["perkIds"] for element in current_game_info["participants"])

    return list(zip(summoner_names, champions, runes))


def change_champion_id_to_champion_name(champion_id: str, url_to_data: str) -> str:
    champion_data = f"{url_to_data}{champion_id}.json"
    return requests.get(champion_data).json()["name"]


def change_player_rune_ids_to_rune_names(rune_ids: list[int], url_to_data: str) -> tuple[str]:
    runes_data = requests.get(url_to_data).json()
    return tuple(
        "".join((section["name"] for section in runes_data if section["id"] == rune_id))
        for rune_id in rune_ids
    )
