
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
  pip install -r requirements.txt
```

Start the program

```bash
  python main.py
```


## Example output

```json
{
    "summonerName0": {
        "championName": "Irelia",
        "runesNames": [
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
    "summonerName1": {
        "championName": "Wukong",
        "runesNames": [
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
    "summonerName2": {
        "championName": "Katarina",
        "runesNames": [
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
    "summonerName3": {
        "championName": "Draven",
        "runesNames": [
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
    "summonerName4": {
        "championName": "Senna",
        "runesNames": [
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
    "summonerName5": {
        "championName": "Talon",
        "runesNames": [
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
    "summonerName6": {
        "championName": "Zed",
        "runesNames": [
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
    "summonerName7": {
        "championName": "Ezreal",
        "runesNames": [
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
    "summonerName8": {
        "championName": "Twitch",
        "runesNames": [
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
    "summonerName9": {
        "championName": "Renekton",
        "runesNames": [
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

