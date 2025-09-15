import requests
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import date

your_teams = ['Milwaukee Brewers']
your_enemy_teams = ['Chicago Cubs']
timezone = "America/Chicago"

def get_pitcher_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats"
    params = {
        "stats": "season",
        "group": "pitching"
    }
    resp = requests.get(url, params=params)
    data = resp.json()

    stats = data.get("stats", [])
    if not stats:
        return {}

    splits = stats[0].get("splits", [])
    if not splits:
        return {}

    stat_line = splits[0].get("stat", {})
    return {
        "wins": stat_line.get("wins", 0),
        "losses": stat_line.get("losses", 0),
        "era": stat_line.get("era", 0.0),
        "strikeouts": stat_line.get("strikeouts", 0)
    }

def upcoming_games(date, type):
    url = "https://statsapi.mlb.com/api/v1/schedule"
    params = {
        "sportId": 1,
        "date": date,
        "hydrate": "probablePitcher(note),broadcasts"
    }
    response = requests.get(url, params=params)
    data = response.json()
    games = data.get("dates", [{}])[0].get("games", [])

    if type == 'my teams':
        teams = your_teams
    elif type == 'enemy teams':
        teams = your_enemy_teams

    game_rows = []

    for game in games:
        game_time_utc_str = game.get("gameDate")
        game_time_utc = datetime.strptime(game_time_utc_str, "%Y-%m-%dT%H:%M:%SZ")
        game_time_utc = game_time_utc.replace(tzinfo=ZoneInfo("UTC"))
        game_time_ct = game_time_utc.astimezone(ZoneInfo(timezone))

        home_team = game["teams"]["home"]["team"]["name"]
        away_team = game["teams"]["away"]["team"]["name"]

        if home_team in teams or away_team in teams:

            # Probable pitchers + IDs
            home_pitcher_data = game["teams"]["home"].get("probablePitcher")
            away_pitcher_data = game["teams"]["away"].get("probablePitcher")

            home_pitcher = home_pitcher_data.get("fullName", "TBD") if home_pitcher_data else "TBD"
            home_pitcher_id = home_pitcher_data.get("id") if home_pitcher_data else None

            away_pitcher = away_pitcher_data.get("fullName", "TBD") if away_pitcher_data else "TBD"
            away_pitcher_id = away_pitcher_data.get("id") if away_pitcher_data else None

            # Fetch stats if IDs exist
            home_stats = get_pitcher_stats(home_pitcher_id) if home_pitcher_id else {}
            away_stats = get_pitcher_stats(away_pitcher_id) if away_pitcher_id else {}

            broadcasts = game.get("broadcasts", [])
            networks = ", ".join([b.get("name") for b in broadcasts if b.get("name")]) or "TBD"

            game_rows.append({
                "away_team": away_team,
                "home_team": home_team,
                "away_pitcher": away_pitcher,
                "away_wins": away_stats.get("wins"),
                "away_losses": away_stats.get("losses"),
                "away_era": away_stats.get("era"),
                "home_pitcher": home_pitcher,
                "home_wins": home_stats.get("wins"),
                "home_losses": home_stats.get("losses"),
                "home_era": home_stats.get("era"),
                "game_time_ct": game_time_ct.strftime("%Y-%m-%d %I:%M %p"),
                "networks": networks
            })

    df = pd.DataFrame(game_rows)
    return df

# Get current date
today = date.today()
# Format as YYYY-MM-DD
today_formatted = today.strftime("%Y-%m-%d")
df_your_teams = upcoming_games(today_formatted,'my teams')
df_your_teams.to_json("JSON/upcoming_your_teams.json", orient="records", indent=4)
df_enemy_teams = upcoming_games(today_formatted,'enemy teams')
df_enemy_teams.to_json("JSON/upcoming_enemy_teams.json", orient="records", indent=4)
print("Saved MLB upcoming games")
