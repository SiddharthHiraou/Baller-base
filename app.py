from flask import Flask, render_template, request
import psycopg2
import pandas as pd

app = Flask(__name__)

# DB Connection Details (Modify accordingly)
conn = psycopg2.connect(
    host="localhost",
    database="NBA_Final",
    user="postgres",  
    password="6666" 
)

# Predefined Queries Dictionary
predefined_queries = {
    "1": """SELECT gd.player_id, pd.player_name, t.nickname AS team, gd.pts, gd.game_id
            FROM gamedetails gd
            JOIN playerdetails pd ON gd.player_id = pd.player_id
            JOIN teams t ON gd.team_id = t.team_id
            WHERE gd.pts > 30;""",
    "2": """SELECT gd.season, t.nickname, ROUND(AVG(gd.fg3m), 2) AS avg_3ptrs
            FROM gamedetails gd
            JOIN playerdetails pd ON gd.player_id = pd.player_id
            JOIN teams t ON gd.team_id = t.team_id
            WHERE pd.player_name = 'Stephen Curry'
            GROUP BY gd.season, t.nickname
            ORDER BY gd.season;""",
    "3": """SELECT g.game_date_est, g.season, g.home_team_id, th.nickname AS home_team, rh.w AS home_wins, rh.l AS home_losses,
                    g.visitor_team_id, tv.nickname AS visitor_team, rv.w AS visitor_wins, rv.l AS visitor_losses
             FROM games g
             JOIN teams th ON g.home_team_id = th.team_id
             JOIN teams tv ON g.visitor_team_id = tv.team_id
             JOIN ranking rh ON rh.team_id = g.home_team_id AND rh.standingsdate = g.game_date_est
             JOIN ranking rv ON rv.team_id = g.visitor_team_id AND rv.standingsdate = g.game_date_est
             WHERE ((g.home_team_id = 1610612747 AND g.visitor_team_id = 1610612738) OR (g.home_team_id = 1610612738 AND g.visitor_team_id = 1610612747))
             ORDER BY g.game_date_est DESC
             LIMIT 5;""",
    "4": """SELECT g.season, g.home_team_id, t.nickname, COUNT(*) AS home_wins
             FROM games g
             JOIN teams t ON g.home_team_id = t.team_id
             WHERE g.home_team_wins = TRUE
             GROUP BY g.season, g.home_team_id, t.nickname
             HAVING COUNT(*) = (
                 SELECT MAX(wins)
                 FROM (
                     SELECT COUNT(*) AS wins
                     FROM games
                     WHERE home_team_wins = TRUE AND season = g.season
                     GROUP BY home_team_id
                 ) AS season_wins
             )
             ORDER BY g.season;""",
    "5": """SELECT pd.player_name, ROUND(AVG(gd.pts),2) AS player_avg,
                   (SELECT ROUND(AVG(pts),2) FROM gamedetails WHERE season=2017) AS season_avg
            FROM gamedetails gd
            JOIN playerdetails pd ON gd.player_id = pd.player_id
            WHERE gd.season = 2017
            GROUP BY pd.player_name
            HAVING AVG(gd.pts) > (SELECT AVG(pts) FROM gamedetails)
            ORDER BY player_avg DESC
            LIMIT 10;"""
}


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predefined_query", methods=["POST"])
def predefined_query():
    query_id = request.form["predefined_query_id"]
    query = predefined_queries.get(query_id)
    if query:
        try:
            df = pd.read_sql_query(query, conn)
            result = df.to_html(classes="table table-striped", index=False)
            return render_template("index.html", result=result, executed_query=query)
        except Exception as e:
            return render_template("index.html", error=str(e))
    else:
        return render_template("index.html", error="❌ Invalid Predefined Query Selected")


@app.route("/insert_data", methods=["POST"])
def insert_data():
    table = request.form["table"]
    values = request.form["values"]
    query = f"INSERT INTO {table} VALUES ({values})"
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        return render_template("index.html", result="✅ Data Inserted Successfully!")
    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route("/predefined_query", methods=["POST"])
def predefined_query():
    query_id = request.form["predefined_query_id"]
    query = predefined_queries.get(query_id)
    if query:
        try:
            df = pd.read_sql_query(query, conn)
            result = df.to_html(classes="table table-striped", index=False)
            return render_template("index.html", result=result)
        except Exception as e:
            return render_template("index.html", error=str(e))
    else:
        return render_template("index.html", error="❌ Invalid Predefined Query Selected")


if __name__ == "__main__":
    app.run(debug=True)