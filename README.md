🧪 Sample SQL Queries
1. ➕ Insert: New NBA team (Buffalo Bills)
sql
Copy
Edit
INSERT INTO teams (...) VALUES (
  1610612770, 1995, 'BNY', 'Bills', 2025, 'Buffalo',
  'Bills Arena', 10000, 'Jeffrey Gundlach', 'Tom Brady',
  'Josh Allen', 'Buffalo Bills'
);
2. 🔄 Update: Elon Musk buys the team
sql
Copy
Edit
UPDATE teams SET owner = 'Elon Musk' WHERE team_id = 1610612770;
3. ❌ Delete: Remove Buffalo team
sql
Copy
Edit
DELETE FROM teams WHERE abbreviation = 'BNY';
4. 🔝 Players with >30 PTS in a game
sql
Copy
Edit
SELECT gd.player_id, pd.player_name, t.nickname, gd.pts
FROM gamedetails gd
JOIN playerdetails pd ON gd.player_id = pd.player_id
JOIN teams t ON gd.team_id = t.team_id
WHERE gd.pts > 30;
5. 🎯 Stephen Curry 3PT Avg per Season
sql
Copy
Edit
SELECT gd.season, t.nickname, ROUND(AVG(gd.fg3m), 2) AS avg_3ptrs
FROM gamedetails gd
JOIN playerdetails pd ON gd.player_id = pd.player_id
JOIN teams t ON gd.team_id = t.team_id
WHERE pd.player_name = 'Stephen Curry'
GROUP BY gd.season, t.nickname ORDER BY gd.season;
🧠 Advanced Query Examples
🥇 Most Home Wins per Season
sql
Copy
Edit
SELECT g.season, g.home_team_id, t.nickname, COUNT(*) as home_wins
FROM games g JOIN teams t ON g.home_team_id = t.team_id
WHERE g.home_team_wins = TRUE
GROUP BY g.season, g.home_team_id, t.nickname
HAVING COUNT(*) = (
    SELECT MAX(wins) FROM (
        SELECT COUNT(*) AS wins
        FROM games
        WHERE home_team_wins = TRUE AND season = g.season
        GROUP BY home_team_id
    ) AS season_wins
)
ORDER BY g.season;
📈 Top 10 Players > 2017 Season Avg
sql
Copy
Edit
SELECT pd.player_name, ROUND(AVG(gd.pts),2) AS player_avg,
       (SELECT ROUND(AVG(pts),2) FROM gamedetails WHERE season=2017) AS season_avg
FROM gamedetails gd
JOIN playerdetails pd ON gd.player_id = pd.player_id
WHERE gd.season = 2017
GROUP BY pd.player_name
HAVING AVG(gd.pts) > (SELECT AVG(pts) FROM gamedetails)
ORDER BY player_avg DESC LIMIT 10;
▶️ Run the App Locally
🔧 Requirements
Python 3.x

PostgreSQL (w/ dataset imported)

Flask

📦 Install Dependencies
bash
Copy
Edit
pip install flask psycopg2-binary
▶️ Launch Web App
bash
Copy
Edit
python app.py
Then open browser at:
http://localhost:5000/

📌 ER Diagram

🧑‍🤝‍🧑 Team
Name	GitHub ID
Siddharth Hiraou	@shiraou
Om Nankar	@omnankar

📂 Dataset Source
🏀 NBA Stats Kaggle Dataset (2003–2022)

📜 License
This repository was developed as part of a final project for educational purposes only.

yaml
Copy
Edit
