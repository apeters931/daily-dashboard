import requests
import pandas as pd

def get_all_team_stats(season="2025"):
    url_teams = "https://statsapi.mlb.com/api/v1/teams"
    teams_response = requests.get(url_teams, params={"sportId": 1})
    teams = teams_response.json()["teams"]

    all_stats = []

    for team in teams:
        team_id = team["id"]
        team_name = team["name"]

        for group in ["hitting", "pitching"]:
            url_stats = "https://statsapi.mlb.com/api/v1/teams/stats"
            params = {
                "season": season,
                "group": group,
                "teamId": team_id
            }
            stats_response = requests.get(url_stats, params=params)
            stats_data = stats_response.json()

            # Defensive coding: check for content
            try:
                stats = stats_data["stats"][0]["splits"][0]["stat"]
                stats["team"] = team_name
                stats["teamId"] = team_id
                stats["group"] = group
                all_stats.append(stats)
            except (IndexError, KeyError):
                print(f"No {group} stats for {team_name}")

    return pd.DataFrame(all_stats)

# 🔁 Run it
df_team_stats = get_all_team_stats()

# 🧪 Preview
print(df_team_stats.head())

# 💾 Save to CSV or JSON
#df_team_stats.to_csv("mlb_team_stats_2025.csv", index=False)
# or:
df_team_stats.to_json("mlb_team_stats_2025.json", orient="records", indent=2)
