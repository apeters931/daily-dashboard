// A list of the JSON files to fetch.
// Update these paths if your file names or directory structure changes.
const jsonFiles = [
    './JSON/hourly_weather.json',
    './JSON/weekly_forecast.json',
    './JSON/upcoming_your_team.json',
    './JSON/upcoming_enemy_teams.json',
    './JSON/brewers_game_log.json',
    './JSON/brewers_game_log.json',
    './JSON/brewers_inning_scores.json',
    './JSON/brewers_pitching_stats.json',
    './JSON/brewers_hitting_stats.json',
    
    // Add any other JSON files you have in the JSON directory
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
        } else if (filePath.includes('weekly') || filePath.includes('14_day')) {
            targetElementId = 'weekly-weather';
        } else if (filePath.includes('upcoming')) {
            targetElementId = 'upcoming-games';
        } else if (filePath.includes('yesterdays')) {
            targetElementId = 'yesterday-games';
        }

        const container = document.getElementById(targetElementId);
        if (container) {
            // Use JSON.stringify for clean, formatted output
            container.querySelector('pre').textContent = JSON.stringify(jsonData, null, 2);
        } else {
            console.error(`Could not find a container for file: ${filePath}`);
        }

    } catch (error) {
        console.error("Failed to fetch or display JSON:", error);
        // Display error message on the page
        const errorContainer = document.getElementById('error-messages');
        if (errorContainer) {
            errorContainer.textContent += `\nError loading ${filePath}: ${error.message}`;
        }
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