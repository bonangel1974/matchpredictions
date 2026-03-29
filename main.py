from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = "df937b3818fbbb2af5dc5e1512d5aeaf"

LEAGUES = {
    "bundesliga": 78,
    "switzerland": 207,
    "austria": 218,
    "seriea": 135,
    "ligue1": 61,
    "premierleague": 39,
    "championsleague": 2,
    "euro": 4,
    "worldcup": 1
}

BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}


@app.route("/")
def home():

    league_key = request.args.get("league", "bundesliga")
    league_id = LEAGUES.get(league_key, 78)
    season = 2024

    # 🔥 1. LIVE + UPCOMING MATCHES
    fixtures_url = f"{BASE_URL}/fixtures?league={league_id}&season={season}&next=5"
    fixtures = requests.get(fixtures_url, headers=headers).json()

    matches = []

    for m in fixtures["response"]:
        matches.append({
            "home": m["teams"]["home"]["name"],
            "away": m["teams"]["away"]["name"],
            "home_logo": m["teams"]["home"]["logo"],
            "away_logo": m["teams"]["away"]["logo"],
            "date": m["fixture"]["date"],
        })

    # 🔥 2. TABLE
    standings_url = f"{BASE_URL}/standings?league={league_id}&season={season}"
    standings = requests.get(standings_url, headers=headers).json()

    table = []

    try:
        for t in standings["response"][0]["league"]["standings"][0][:10]:
            table.append({
                "rank": t["rank"],
                "team": t["team"]["name"],
                "logo": t["team"]["logo"],
                "points": t["points"]
            })
    except:
        pass

    # 🔥 3. TOP SCORERS
    scorers_url = f"{BASE_URL}/players/topscorers?league={league_id}&season={season}"
    scorers_data = requests.get(scorers_url, headers=headers).json()

    scorers = []

    for p in scorers_data["response"][:10]:
        scorers.append({
            "name": p["player"]["name"],
            "team": p["statistics"][0]["team"]["name"],
            "goals": p["statistics"][0]["goals"]["total"]
        })

    return render_template(
        "index.html",
        matches=matches,
        table=table,
        scorers=scorers,
        league=league_key
    )


if __name__ == "__main__":
    app.run(debug=True)