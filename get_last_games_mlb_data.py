import requests

# schedule_url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2025-09-08"
# schedule_resp = requests.get(schedule_url).json()

# for game in schedule_resp['dates'][0]['games']:
#     print(f"{game['teams']['away']['team']['name']} @ {game['teams']['home']['team']['name']}")
#     print(f"  gamePk: {game['gamePk']}")
#     code = game['status'].get('code', 'N/A')
#     print(f"  Game Status: {game['status']['detailedState']} ({code})")
#     print()

import json
import requests

game_pk = 776406
url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))  # Pretty-print it
else:
    print(f"Error: {response.status_code}")

with open("boxscore.json", "w") as f:
    json.dump(data, f, indent=2)

