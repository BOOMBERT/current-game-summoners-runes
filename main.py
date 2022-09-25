import requests


with open("api_key", "r", encoding="utf-8") as file:
    MY_API_KEY = file.read()

API_ENDPOINTS = {
    "get_summoner_info":
        'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/',
    "get_current_game_info":
        'https://eun1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'
}


class Summoner:

    def __init__(self, username, summoner_info_api, current_game_info_api, api_key):
        self.username = username
        self.summoner_info_api = summoner_info_api
        self.current_game_info_api = current_game_info_api
        self._api_key = api_key
        self._summoner_id = None

    def _get_summoner_info(self):
        summoner_info_request = requests.get(
            url=f"{self.summoner_info_api}{self.username}",
            params={
                "api_key": self._api_key
            })

        if summoner_info_request.ok:
            _summoner_info = summoner_info_request.json()
            self._summoner_id = _summoner_info["id"]

            return _summoner_info

        if summoner_info_request.status_code == 404:
            print("Summoner with this username does not exist")

        else:
            try:
                summoner_info_request.raise_for_status()
            except requests.exceptions.RequestException as error:
                print("Request Error:", error)

        return None

    # def _get_current_game_info(self):
    #     try:
    #         current_game_info_request = requests.get(
    #         url=f"{self.current_game_info_api}{self._summoner_id}",
    #             params={
    #                 "api_key": self._api_key
    #             })


# def check_player(username):
#     summoner = Summoner(
#         username,
#         API_ENDPOINTS["get_summoner_info"], API_ENDPOINTS["get_current_game_info"], MY_API_KEY)


if __name__ == "__main__":
    pass
    #check_player("")
