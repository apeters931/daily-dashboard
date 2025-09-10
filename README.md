# Daily Dashboard

## Sports
- Your teams
- Football (when in season)
- Baseball (when in season)
- Basketball (when in season)
- College football (when in season)
- College basketball (when in season)

## Finance
- Performance of your investments

## Local News
- Weather
- Headlines with LLM summaries & link to full article
- Upcoming events

## National News
- Headlines with LLM summaries & link to full article

## Arts & Entertainment
- Charts (music, movies, books)
- New / upcoming releases (music & movies)
- Reviews (music & movies)
- Shows in your area / shows of groups you're interested in?


# For Developing

`python3 -m http.server 8000`

`http://localhost:8000/sports.html`


## Instructions

✅ How to Handle Multiple JSON Files

Generate multiple JSON files in your workflow

Your Python script can write more than one file.

Example:

site/data/players.json
site/data/teams.json
site/data/stats.json


Deploy everything under /site

- name: Run Python script to generate JSON
  run: |
    mkdir -p site/data
    python scripts/make_players.py -o site/data/players.json
    python scripts/make_teams.py -o site/data/teams.json
    python scripts/make_stats.py -o site/data/stats.json


Deploy to GitHub Pages (all files, not just JSON)

- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./site
    publish_branch: gh-pages

📂 Example Folder Layout
repo-root/
├── site/                  # published to GitHub Pages
│   ├── index.html
│   ├── script.js
│   └── data/
│       ├── players.json
│       ├── teams.json
│       └── stats.json
├── scripts/
│   ├── make_players.py
│   ├── make_teams.py
│   └── make_stats.py
└── .github/workflows/deploy.yml

🌐 URLs

After deployment, your files would be available at:

https://<username>.github.io/<repo>/index.html

https://<username>.github.io/<repo>/data/players.json

https://<username>.github.io/<repo>/data/teams.json

https://<username>.github.io/<repo>/data/stats.json

🎯 Fetching them in client-side JS
async function loadData() {
  const players = await fetch('data/players.json').then(r => r.json());
  const teams = await fetch('data/teams.json').then(r => r.json());
  const stats = await fetch('data/stats.json').then(r => r.json());

  console.log(players, teams, stats);
}
loadData();


👉 So the answer is: you don’t need a different setup. Just generate all the JSON files into your published folder (e.g., site/), and GitHub Pages will happily serve all of them.