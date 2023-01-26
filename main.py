from typing import List, Any, Generator
from os import getenv
import json
from dotenv import load_dotenv

import references
import request_operations
import operations_on_data


class InitialSummoner:
    def __init__(self, data_with_info) -> None:
        self._data_with_info = data_with_info

    def get_id(self) -> str:
        try:
            return self._data_with_info["id"]

        except KeyError as key_error:
            raise SystemExit("ID not found") from key_error

        except TypeError as type_error:
            raise SystemExit("Wrong data") from type_error


class Summoner:
    def __init__(self, name: str, champion_name: str, runes_names: List[str]) -> None:
        self.name = name
        self.champion_name = champion_name
        self.runes_names = runes_names

    @classmethod
    def info_with_changed_ids_to_names(
            cls, name: str, champion_id: int, runes_ids: List[int]
    ) -> "Summoner":
        champion_name = operations_on_data.change_champion_id_to_champion_name(champion_id)
        runes_names = operations_on_data.change_player_runes_ids_to_runes_names(runes_ids)

        return cls(name, champion_name, runes_names)


class CurrentGameInfo:
    _summoners_info = {}

    def __init__(self, data_with_info) -> None:
        self._data_with_info = data_with_info

    def get_specific_info(
            self, first_key_name: str, second_key_name: str = ""
    ) -> Generator[Any, Any, None]:
        elements_with_info = self._data_with_info["participants"]
        return (
            (
                element[first_key_name][second_key_name]
                for element in elements_with_info
            )
            if second_key_name
            else (
                element[first_key_name]
                for element in elements_with_info
            )
        )

    def add_summoner_needed_info(self, summoner: Summoner) -> None:
        self._summoners_info[summoner.name] = {
            "championName": summoner.champion_name,
            "runesNames": summoner.runes_names
        }

    def result_with_summoners_info(self) -> str | None:
        if not self._summoners_info:
            print("The summoners info is empty")
            return None

        return json.dumps(self._summoners_info, indent=4, ensure_ascii=False)


def get_checked_info_from_authorized_api_request(
        api_url: str, info_to_request: str, api_key: str
) -> str | None:
    response_from_request = request_operations.get_info_from_authorized_api_request(
        api_url, info_to_request, api_key
    )
    if request_operations.check_the_request_for_error(response_from_request):
        return response_from_request.json()

    return None


def add_needed_changed_summoner_info_to_current_game_info(
        current_game: CurrentGameInfo
) -> None:
    SUMMONERS_NAMES_KEY = "summonerName"
    CHAMPIONS_NAMES_KEY = "championId"
    RUNES_NAMES_KEY = ("perks", "perkIds")

    try:
        for name, champion_id, runes_ids in zip(
                current_game.get_specific_info(
                    first_key_name=SUMMONERS_NAMES_KEY
                ),
                current_game.get_specific_info(
                    first_key_name=CHAMPIONS_NAMES_KEY
                ),
                current_game.get_specific_info(
                    first_key_name=RUNES_NAMES_KEY[0],
                    second_key_name=RUNES_NAMES_KEY[1]
                )
        ):
            current_game.add_summoner_needed_info(
                Summoner.info_with_changed_ids_to_names(name, champion_id, runes_ids)
            )

    except KeyError as key_error:
        raise SystemExit("Data problem") from key_error


class Application:
    def __init__(self, summoner_name: str, region: str) -> None:
        self.summoner_name = summoner_name
        self.region = region
        self._summoner_id = None
        self._current_game_info = None

    def get_initial_summoner_id(self) -> None:
        summoner_api_url: str = \
            references.API_ENDPOINTS["get_summoner_info"].replace(" ", self.region)

        initial_summoner = InitialSummoner(
            get_checked_info_from_authorized_api_request(
                api_url=summoner_api_url,
                info_to_request=self.summoner_name,
                api_key=getenv("API_KEY")
            )
        )
        self._summoner_id = initial_summoner.get_id()

    def get_current_game_info(self) -> None:
        current_game_api_url: str = \
            references.API_ENDPOINTS["get_current_game_info"].replace(" ", self.region)

        self._current_game_info = CurrentGameInfo(
            get_checked_info_from_authorized_api_request(
                api_url=current_game_api_url,
                info_to_request=self._summoner_id,
                api_key=getenv("API_KEY")
            )
        )

    def check_the_summoner_current_game(self) -> None:
        self.get_initial_summoner_id()
        self.get_current_game_info()

        add_needed_changed_summoner_info_to_current_game_info(self._current_game_info)
        print(self._current_game_info.result_with_summoners_info())


def main() -> None:
    load_dotenv()
    REGIONS = ("BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1", "RU", "TR1")

    while (region_name := input(f"{', '.join(REGIONS)}\nEnter the region name -> ")).upper() \
            not in REGIONS:
        print("Unknown region")

    summoner_name = input("Enter the summoner's name -> ")

    app = Application(summoner_name, region_name)
    app.check_the_summoner_current_game()


if __name__ == "__main__":
    main()
