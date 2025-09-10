import requests
import pandas as pd
from time import sleep

def get_all_teams():
    url = "https://statsapi.mlb.com/api/v1/teams"
    params = {"sportId": 1}
    response = requests.get(url, params=params)
    data = response.json()
    return data["teams"]

def get_team_roster(team_id):
    url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
    response = requests.get(url)
    data = response.json()
    return data.get("roster", [])

def get_player_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats"
    params = {
        "stats": "season",
        "group": "hitting,pitching"
    }
    response = requests.get(url, params=params)
    data = response.json()

    stats = {}
    splits = data.get("stats", [])
    for group in splits:
        if group.get("group", {}).get("displayName") in ["hitting", "pitching"]:
            if group.get("splits"):
                stat_line = group["splits"][0].get("stat", {})
                stats.update(stat_line)
    return stats

def get_all_player_stats():
    teams = get_all_teams()
    all_data = []

    for team in teams:
        team_id = team["id"]
        team_name = team["name"]
        print(f"Fetching roster for {team_name}...")

        roster = get_team_roster(team_id)

        for player in roster:
            player_id = player["person"]["id"]
            player_name = player["person"]["fullName"]
            position = player["position"]["abbreviation"]

            print(f"  Getting stats for {player_name} ({position})")

            stats = get_player_stats(player_id)

            player_data = {
                "team": team_name,
                "player_name": player_name,
                "player_id": player_id,
                "position": position,
                **stats
            }

            all_data.append(player_data)

            # Sleep briefly to avoid hammering the API
            sleep(0.3)

    return pd.DataFrame(all_data)

# 🔁 Run it
df = get_all_player_stats()

# 🧪 Preview
print(df.head())

# 💾 Save to JSON
df.to_json("mlb_player_stats_2025.json", orient="records", indent=2)
