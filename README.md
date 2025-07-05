# 🏀 Baller Base – NBA Relational Database & Web Portal

A fully normalized, query-optimized relational database system for analyzing NBA game statistics (2003–2022). Built as a final project for the **CSE587: Data Models and Query Languages** course.

---

## 📌 Objective

The goal of **Baller Base** is to move beyond spreadsheets and build a robust, scalable **PostgreSQL database** that enables efficient **storage, retrieval, and analysis** of NBA data — including player performance, team stats, game outcomes, and league rankings.

Use cases:
- 🧠 NBA Analysts & Coaches: KPI dashboards & team strategy
- 🏀 Fans & Stat Enthusiasts: Compare players across seasons
- 🧮 Developers: Learn schema design, normalization & Flask UI

---

## 🧱 Schema Design & Normalization

The database is constructed with **6 core tables**, designed using **BCNF/3NF normalization principles**, and validated using **functional dependencies**.

| Table           | Description                                      | Normal Form |
|----------------|--------------------------------------------------|-------------|
| `Teams`         | Team info, city, arena, owner                   | ✅ BCNF     |
| `Players`       | Player ID, team, season                         | ✅ 3NF (w/ Unique ID) |
| `PlayerDetails` | Unique mapping of Player ID to Player Name      | ✅ BCNF     |
| `Games`         | Game metadata: home/away, score, date, status   | ✅ BCNF     |
| `GameDetails`   | Player game stats (PTS, AST, FG3M, etc.)        | ✅ 3NF      |
| `Ranking`       | Standings per season (W/L, conference, % wins)  | ✅ 3NF      |

---

## 🧹 Data Cleaning & Challenges Solved

🛠 Key preprocessing fixes:
- Created a **`UNIQUE_ID`** combining `Player_ID + Team_ID + Season` to handle duplicates
- Fixed inconsistent name formats (e.g., "OJ Mayo" vs "O.J. Mayo")
- Enforced referential integrity by resolving duplicate or missing foreign keys
- Resolved PostgreSQL datatype issues (e.g., `YEAR` to `INT`)
- Added constraints: `NOT NULL`, range checks (`0 <= W_PCT <= 1`), valid foreign key mapping

---

## ⚙️ Tech Stack

| Layer     | Technology             |
|-----------|------------------------|
| Database  | PostgreSQL (via pgAdmin) |
| Backend   | Python Flask           |
| Frontend  | HTML5 + Bootstrap 5    |
| Hosting   | Localhost Flask App    |
| Dataset   | Kaggle NBA Stats (2003–2022) |

---

## 🌐 Web App UI

An interactive web portal to:
- 🧮 Run ad hoc SQL queries
- 📥 Insert records into 6 tables
- 📊 Execute 5+ predefined KPI queries

> Example screenshot:  
> ![Web UI Sample](screenshots/ui_sample.png)

---

## 💡 Key Features

- ✅ Fully normalized database (BCNF/3NF)
- 🚀 PostgreSQL indexing for speed (↓ from 31ms → 1ms)
- 🔎 Predefined KPIs available from dropdown
- 🧪 `EXPLAIN ANALYZE` used to optimize real queries
- 📈 Supports 668,000+ game records and 200K+ rankings

---

## ⚡ Indexing & Query Optimization

```sql
-- Indexing to improve join & filter speed
CREATE INDEX idx_games_details_player_id ON gamedetails(player_id);
CREATE INDEX idx_games_details_game_id ON gamedetails(game_id);
CREATE INDEX idx_ranking_team_id ON ranking(team_id);
CREATE INDEX idx_players_player_id ON players(player_id);
