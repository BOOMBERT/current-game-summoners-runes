
# Current game summoners runes

This program is used to getting the runes of all summoners from the current game of the selected player in the game league of legends. The output is in JSON format.


## Environment Variables

To run this project, you will need to add the following environment variable to your .env file.

`API_KEY="Enter the api key here from https://developer.riotgames.com"`


## Run Locally

Clone the project

```bash
  git clone https://github.com/BOOMBERT/current-game-summoners-runes.git
```

Go to the project directory

```bash
  cd current-game-summoners-runes
```

Install the necessary libraries

```bash
  pip install python-dotenv
  pip install requests
```

Start the program

```bash
  python main.py
```


## Example output

```json
{
    "summoner_name0": {
        "champion_name": "Irelia",
        "rune_names": [
            "Conqueror",
            "Triumph",
            "Legend: Alacrity",
            "Last Stand",
            "Bone Plating",
            "Unflinching",
            "Attack Speed",
            "Adaptive Force",
            "Armor"
        ]
    },
    "summoner_name1": {
        "champion_name": "Wukong",
        "rune_names": [
            "Conqueror",
            "Triumph",
            "Legend: Tenacity",
            "Cut Down",
            "Sudden Impact",
            "Relentless Hunter",
            "Attack Speed",
            "Adaptive Force",
            "Armor"
        ]
    },
    "summoner_name2": {
        "champion_name": "Katarina",
        "rune_names": [
            "Conqueror",
            "Triumph",
            "Legend: Tenacity",
            "Last Stand",
            "Sudden Impact",
            "Relentless Hunter",
            "Adaptive Force",
            "Adaptive Force",
            "Armor"
        ]
    },
    "summoner_name3": {
        "champion_name": "Draven",
        "rune_names": [
            "Lethal Tempo",
            "Triumph",
            "Legend: Alacrity",
            "Coup de Grace",
            "Absolute Focus",
            "Gathering Storm",
            "Attack Speed",
            "Adaptive Force",
            "Armor"
        ]
    },
    "summoner_name4": {
        "champion_name": "Senna",
        "rune_names": [
            "Grasp of the Undying",
            "Demolish",
            "Conditioning",
            "Overgrowth",
            "Magical Footwear",
            "Approach Velocity",
            "Adaptive Force",
            "Adaptive Force",
            "Health Scaling"
        ]
    },
    "summoner_name5": {
        "champion_name": "Talon",
        "rune_names": [
            "First Strike",
            "Magical Footwear",
            "Future's Market",
            "Cosmic Insight",
            "Waterwalking",
            "Nimbus Cloak",
            "Attack Speed",
            "Adaptive Force",
            "Armor"
        ]
    },
    "summoner_name6": {
        "champion_name": "Zed",
        "rune_names": [
            "Electrocute",
            "Taste of Blood",
            "Eyeball Collection",
            "Ultimate Hunter",
            "Scorch",
            "Transcendence",
            "Adaptive Force",
            "Adaptive Force",
            "Magic Resist"
        ]
    },
    "summoner_name7": {
        "champion_name": "Ezreal",
        "rune_names": [
            "First Strike",
            "Magical Footwear",
            "Biscuit Delivery",
            "Cosmic Insight",
            "Transcendence",
            "Gathering Storm",
            "Attack Speed",
            "Adaptive Force",
            "Armor"
        ]
    },
    "summoner_name8": {
        "champion_name": "Twitch",
        "rune_names": [
            "Hail of Blades",
            "Taste of Blood",
            "Eyeball Collection",
            "Treasure Hunter",
            "Legend: Alacrity",
            "Coup de Grace",
            "Adaptive Force",
            "Adaptive Force",
            "Armor"
        ]
    },
    "summoner_name9": {
        "champion_name": "Renekton",
        "rune_names": [
            "Press the Attack",
            "Triumph",
            "Legend: Tenacity",
            "Last Stand",
            "Bone Plating",
            "Unflinching",
            "Adaptive Force",
            "Adaptive Force",
            "Armor"
        ]
    }
}
```


## Authors

- [@BOOMBERT](https://github.com/BOOMBERT)


## License

[MIT](https://choosealicense.com/licenses/mit/)

