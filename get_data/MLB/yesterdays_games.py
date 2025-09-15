import requests
import json
import os
from datetime import date, timedelta

def get_full_game_json(date, team_to_find):
    """
    Fetches the full JSON data for a specific MLB game by searching for a single team.

    Args:
        date (str): The date of the game in 'YYYY-MM-DD' format.
        team_to_find (str): The name of the team to find in the schedule (e.g., 'Brewers').

    Returns:
        tuple or None: A tuple containing the full JSON data for the game, home team name,
                       and away team name, or None if the game is not found or an error occurs.
    """
    schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date}"
    
    try:
        response = requests.get(schedule_url)
        response.raise_for_status()
        schedule_data = response.json()
        
        game_pk = None
        home_team = None
        away_team = None
        
        if 'dates' in schedule_data and schedule_data['dates']:
            for game in schedule_data['dates'][0]['games']:
                api_home = game['teams']['home']['team']['name']
                api_away = game['teams']['away']['team']['name']
                
                if team_to_find.lower() in api_home.lower():
                    game_pk = game['gamePk']
                    home_team = api_home
                    away_team = api_away
                    break
                elif team_to_find.lower() in api_away.lower():
                    game_pk = game['gamePk']
                    home_team = api_home
                    away_team = api_away
                    break
        
        if not game_pk:
            print(f"Error: Game not found for {team_to_find} on {date}.")
            return None, None, None

        live_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
        live_response = requests.get(live_url)
        live_response.raise_for_status()
        
        return live_response.json(), home_team, away_team

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching game data: {e}")
        return None, None, None

def get_inning_runs(game_json, home_team_name, away_team_name):
    """
    Extracts the runs, hits, and errors by inning for each team, calculates the totals,
    and returns the data as a dictionary.

    Args:
        game_json (dict): A dictionary containing the full game data.
        home_team_name (str): The name of the home team.
        away_team_name (str): The name of the away team.

    Returns:
        dict: A dictionary with inning-by-inning scores and the final score for both teams.
    """
    try:
        linescore = game_json.get('liveData', {}).get('linescore', {})
        
        total_home_hits = linescore.get('teams', {}).get('home', {}).get('hits', 0)
        total_away_hits = linescore.get('teams', {}).get('away', {}).get('hits', 0)
        total_home_errors = linescore.get('teams', {}).get('home', {}).get('errors', 0)
        total_away_errors = linescore.get('teams', {}).get('away', {}).get('errors', 0)
        
        all_plays = game_json.get('liveData', {}).get('plays', {}).get('allPlays', [])
        
        inning_scores = {}
        
        for play in all_plays:
            about = play.get('about', {})
            result = play.get('result', {})
            
            inning_number = about.get('inning')
            away_score = result.get('awayScore')
            home_score = result.get('homeScore')
            
            if inning_number is not None and away_score is not None and home_score is not None:
                inning_scores[inning_number] = {
                    'away_score': away_score,
                    'home_score': home_score
                }
        
        structured_output = {
            'game_summary': {
                'away_team': away_team_name,
                'home_team': home_team_name
            },
            'inning_scores': []
        }
        
        prev_away_runs = 0
        prev_home_runs = 0
        
        sorted_innings = sorted(inning_scores.keys())
        for inning_num in sorted_innings:
            current_away_runs = inning_scores[inning_num]['away_score']
            current_home_runs = inning_scores[inning_num]['home_score']
            
            inning_data = {
                'inning': inning_num,
                'away_runs': current_away_runs - prev_away_runs,
                'home_runs': current_home_runs - prev_home_runs
            }
            structured_output['inning_scores'].append(inning_data)
            
            prev_away_runs = current_away_runs
            prev_home_runs = current_home_runs

        total_away_runs = linescore.get('teams', {}).get('away', {}).get('runs', 0)
        total_home_runs = linescore.get('teams', {}).get('home', {}).get('runs', 0)

        structured_output['final_score'] = {
            'away_runs': total_away_runs,
            'home_runs': total_home_runs,
            'away_hits': total_away_hits,
            'home_hits': total_home_hits,
            'away_errors': total_away_errors,
            'home_errors': total_home_errors
        }
        
        return structured_output

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}

def get_player_hitting_stats(game_json):
    """
    Extracts the batting statistics for every player from the game's boxscore.

    Args:
        game_json (dict): A dictionary with the full game data.

    Returns:
        list: A list of dictionaries, where each dictionary contains a player's hitting stats.
    """
    all_players = []
    
    try:
        boxscore = game_json.get('liveData', {}).get('boxscore', {})
        teams = boxscore.get('teams', {})
        
        for team_key in ['away', 'home']:
            team_data = teams.get(team_key, {})
            players_data = team_data.get('players', {})
            
            for player_id, player_stats in players_data.items():
                person = player_stats.get('person', {})
                stats = player_stats.get('stats', {})
                hitting_stats = stats.get('batting', {})
                
                if hitting_stats:
                    player_info = {
                        'full_name': person.get('fullName'),
                        'team_side': team_key,
                        'at_bats': hitting_stats.get('atBats', 0),
                        'hits': hitting_stats.get('hits', 0),
                        'doubles': hitting_stats.get('doubles', 0),
                        'triples': hitting_stats.get('triples', 0),
                        'home_runs': hitting_stats.get('homeRuns', 0),
                        'runs_batted_in': hitting_stats.get('rbi', 0),
                        'walks': hitting_stats.get('baseOnBalls', 0),
                        'strikeouts': hitting_stats.get('strikeOuts', 0)
                    }
                    all_players.append(player_info)
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return all_players
    
def get_pitching_stats(game_json):
    """
    Extracts the pitching statistics for every pitcher from the game's boxscore.

    Args:
        game_json (dict): A dictionary with the full game data.

    Returns:
        list: A list of dictionaries, where each dictionary contains a pitcher's stats.
    """
    all_pitchers = []
    
    try:
        boxscore = game_json.get('liveData', {}).get('boxscore', {})
        teams = boxscore.get('teams', {})
        
        for team_key in ['away', 'home']:
            team_data = teams.get(team_key, {})
            players_data = team_data.get('players', {})
            
            for player_id, player_stats in players_data.items():
                person = player_stats.get('person', {})
                stats = player_stats.get('stats', {})
                pitching_stats = stats.get('pitching', {})
                
                if pitching_stats:
                    pitcher_info = {
                        'full_name': person.get('fullName'),
                        'team_side': team_key,
                        'innings_pitched': pitching_stats.get('inningsPitched', 0),
                        'runs': pitching_stats.get('runs', 0),
                        'earned_runs': pitching_stats.get('earnedRuns', 0),
                        'strikeouts': pitching_stats.get('strikeOuts', 0)
                    }
                    all_pitchers.append(pitcher_info)
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return all_pitchers

if __name__ == "__main__":
    # Get yesterday's date dynamically
    yesterday = date.today() - timedelta(days=1)
    game_date = yesterday.strftime('%Y-%m-%d')
    
    # Define a list of teams to find games for
    teams_to_find = ['Brewers', 'Cubs']
    
    output_directory = 'JSON'
    
    # Create the directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created directory '{output_directory}'")

    for team_name in teams_to_find:
        print(f"\n--- Processing game for {team_name} on {game_date} ---")
        
        game_json, home_team, away_team = get_full_game_json(game_date, team_name)
        
        if game_json:
            # Add team name to all filenames to avoid overwriting
            team_slug = team_name.lower().replace(" ", "_")
            
            # Save the full game log to a file inside the new directory
            game_log_file_path = os.path.join(output_directory, f'{team_slug}_game_log.json')
            with open(game_log_file_path, 'w', encoding='utf-8') as f:
                json.dump(game_json, f, indent=2)
            print(f"Successfully saved raw game data to '{game_log_file_path}'")
            
            # Call the function to get the structured inning data
            game_data_to_save = get_inning_runs(game_json, home_team, away_team)
            
            if game_data_to_save:
                output_file_path = os.path.join(output_directory, f'{team_slug}_inning_scores.json')
                with open(output_file_path, 'w') as outfile:
                    json.dump(game_data_to_save, outfile, indent=4)
                print(f"Successfully saved inning and final scores to '{output_file_path}'")

            # Call the function to get player hitting stats
            player_stats_to_save = get_player_hitting_stats(game_json)
            
            if player_stats_to_save:
                player_stats_file_path = os.path.join(output_directory, f'{team_slug}_player_hitting_stats.json')
                with open(player_stats_file_path, 'w') as player_file:
                    json.dump(player_stats_to_save, player_file, indent=4)
                print(f"Successfully saved player hitting stats to '{player_stats_file_path}'")

            # Call the new function to get pitching stats
            pitching_stats_to_save = get_pitching_stats(game_json)
            
            if pitching_stats_to_save:
                pitching_stats_file_path = os.path.join(output_directory, f'{team_slug}_pitching_stats.json')
                with open(pitching_stats_file_path, 'w') as pitcher_file:
                    json.dump(pitching_stats_to_save, pitcher_file, indent=4)
                print(f"Successfully saved pitching stats to '{pitching_stats_file_path}'")