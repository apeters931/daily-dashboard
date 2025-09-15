// A list of the JSON files to fetch for upcoming games
const upcomingFiles = [
    './JSON/upcoming_your_teams.json',
    './JSON/upcoming_enemy_teams.json'
];

// A list of the JSON files to fetch for weather data
const weatherFiles = [
    './JSON/hourly_weather.json',
    './JSON/weekly_forecast.json'
];

// A list of the JSON files for yesterday's games to be merged
const yesterdayFiles = [
    './JSON/brewers_inning_scores.json',
    './JSON/brewers_player_hitting_stats.json',
    './JSON/brewers_pitching_stats.json',
    './JSON/cubs_inning_scores.json',
    './JSON/cubs_player_hitting_stats.json',
    './JSON/cubs_pitching_stats.json',
];

const fetchAndDisplayJson = async (filePaths, targetElementId) => {
    try {
        const fetchPromises = filePaths.map(filePath => 
            fetch(filePath).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status} for file: ${filePath}`);
                }
                return response.json();
            })
        );

        const jsonData = await Promise.all(fetchPromises);
        
        const container = document.getElementById(targetElementId);
        if (container) {
            container.querySelector('pre').textContent = JSON.stringify(jsonData, null, 2);
        } else {
            console.error(`Could not find a container for ID: ${targetElementId}`);
        }

    } catch (error) {
        console.error("Failed to fetch or display JSON:", error);
    }
};

const fetchAndMergeYesterdayGames = async () => {
    try {
        const fetchPromises = yesterdayFiles.map(filePath =>
            fetch(filePath).then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status} for file: ${filePath}`);
                }
                return response.json();
            })
        );
        
        const jsonDataArray = await Promise.all(fetchPromises);
        
        // Merge the objects from the array into a single object
        const mergedData = jsonDataArray.reduce((acc, curr) => {
            // Check if the key exists and if it is an array. If so, concatenate.
            for (const key in curr) {
                if (Array.isArray(curr[key]) && Array.isArray(acc[key])) {
                    acc[key] = acc[key].concat(curr[key]);
                } else {
                    acc[key] = curr[key];
                }
            }
            return acc;
        }, {});

        const container = document.getElementById('yesterday-games');
        if (container) {
            container.querySelector('pre').textContent = JSON.stringify(mergedData, null, 2);
        } else {
            console.error(`Could not find a container for ID: yesterday-games`);
        }

    } catch (error) {
        console.error("Failed to fetch or merge yesterday's game data:", error);
    }
};

// Run the functions when the page loads
window.onload = () => {
    fetchAndDisplayJson(upcomingFiles, 'upcoming-games');
    fetchAndDisplayJson(weatherFiles, 'weather-content'); // This container is a div, not a pre tag
    fetchAndMergeYesterdayGames();
};