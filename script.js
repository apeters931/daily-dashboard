// Highlight active nav link automatically
document.addEventListener("DOMContentLoaded", () => {
  const currentPage = window.location.pathname.split("/").pop();
  document.querySelectorAll("nav a").forEach(link => {
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active");
    }
  });
});

// Fetch the JSON file and display its data
fetch('mlb_schedule_with_pitchers.json')
.then(response => response.json())
.then(games => {
  const container = document.getElementById('games-list');

  // Loop through each game and create strings
  games.forEach(game => {
    // "home team @ away team"
    const gameString = `${game.away_team} vs ${game.home_team} @ ${game.game_time_ct.split(" ").slice(1).join(" ")}`;
    const awayPitcherString = `${game.away_pitcher} (${game.away_wins}-${game.away_losses}, ${game.away_era} ERA)`;
    const homePitcherString = `${game.home_pitcher} (${game.home_wins}-${game.home_losses}, ${game.home_era} ERA)`;
    const networksString =  `${game.networks}`

    // Create a <p> element and append to container
    const h3 = document.createElement('h3');
    h3.textContent = gameString;
    container.appendChild(h3);

    const p2 = document.createElement('p');
    p2.textContent = awayPitcherString;
    container.appendChild(p2);

    const p3 = document.createElement('p');
    p3.textContent = homePitcherString;
    container.appendChild(p3);

    const p4 = document.createElement('p');
    p4.textContent = networksString;
    container.appendChild(p4);

  });
})
.catch(error => console.error('Error loading JSON:', error));