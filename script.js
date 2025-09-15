// A list of the JSON files to fetch.
const jsonFiles = [
    './JSON/upcoming_enemy_teams.json',
    './JSON/upcoming_your_teams.json',
    './JSON/brewers_inning_scores.json',
    './JSON/brewers_pitching_stats.json',
    './JSON/brewers_player_hitting_stats.json',
    './JSON/cubs_game_log.json',
    './JSON/cubs_inning_scores.json',
    './JSON/cubs_pitching_stats.json',
    './JSON/cubs_player_hitting_stats.json',
    './JSON/weekly_forecast.json',
    './JSON/hourly_weather.json'
];

// Asynchronously fetches and displays a single JSON file
const fetchAndDisplayJson = async (filePath) => {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status} for file: ${filePath}`);
        }
        const jsonData = await response.json();
        
        // Find the appropriate container based on the file name
        let targetElementId;
        if (filePath.includes('hourly')) {
            targetElementId = 'hourly-weather';
        } else if (filePath.includes('weekly')) {
            targetElementId = 'weekly-weather';
        } else if (filePath.includes('upcoming')) {
            targetElementId = 'upcoming-games';
        } else if (filePath.includes('yesterdays') || filePath.includes('game_log')) {
            targetElementId = 'yesterday-games';
        } else if (filePath.includes('hitting_stats')) {
            targetElementId = 'brewers-hitting-stats';
        } else if (filePath.includes('pitching_stats')) {
            targetElementId = 'brewers-pitching-stats';
        } else if (filePath.includes('inning_scores')) {
            targetElementId = 'brewers-inning-scores';
        }

        const container = document.getElementById(targetElementId);
        if (container) {
            container.querySelector('pre').textContent = JSON.stringify(jsonData, null, 2);
        } else {
            console.error(`Could not find a container for file: ${filePath}`);
        }

    } catch (error) {
        console.error("Failed to fetch or display JSON:", error);
    }
};

// Loop through all the JSON files and fetch them
const loadAllJson = () => {
    jsonFiles.forEach(file => {
        fetchAndDisplayJson(file);
    });
};

// Run the function when the page loads
window.onload = loadAllJson;