from flask import Flask, render_template, request
import requests
import os
from datetime import datetime, timedelta, timezone
from team_logos import find_logo

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://api.football-data.org/v4"

HEADERS = {
    "X-Auth-Token": API_KEY
}

LEAGUES = {
    "bundesliga": "BL1",
    "switzerland": "CLI",
    "austria": "BSA",
    "premierleague": "PL",
    "seriea": "SA",
    "ligue1": "FL1",
    "championsleague": "CL",
    "euro": "EC",
    "worldcup": "WC"
}


def format_kickoff(utc_value: str) -> str:
    if not utc_value:
        return "-"
    try:
        dt = datetime.fromisoformat(utc_value.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return utc_value


@app.route("/")
def home():
    league_key = request.args.get("league", "bundesliga")
    league_code = LEAGUES.get(league_key, "BL1")

    matches = []
    table = []
    scorers = []

    try:
        today = datetime.now(timezone.utc).date()
        future = today + timedelta(days=7)

        # MATCHES
        res = requests.get(
            f"{BASE_URL}/competitions/{league_code}/matches?dateFrom={today}&dateTo={future}",
            headers=HEADERS
        )
        data = res.json()

        for m in data.get("matches", [])[:10]:
            home = m["homeTeam"]["name"]
            away = m["awayTeam"]["name"]

            matches.append({
                "home": home,
                "away": away,
                "home_logo": find_logo(home),
                "away_logo": find_logo(away),
                "time": format_kickoff(m["utcDate"])
            })

        # TABLE
        res = requests.get(
            f"{BASE_URL}/competitions/{league_code}/standings",
            headers=HEADERS
        )
        data = res.json()

        standings = data.get("standings", [])
        if standings:
            for row in standings[0]["table"][:10]:
                team = row["team"]["name"]

                table.append({
                    "pos": row["position"],
                    "team": team,
                    "logo": find_logo(team),
                    "points": row["points"]
                })

        # SCORERS
        res = requests.get(
            f"{BASE_URL}/competitions/{league_code}/scorers",
            headers=HEADERS
        )
        data = res.json()

        for s in data.get("scorers", [])[:10]:
            team = s["team"]["name"]

            scorers.append({
                "name": s["player"]["name"],
                "team": team,
                "logo": find_logo(team),
                "goals": s["goals"]
            })

    except Exception as e:
        print("ERROR:", e)

    return render_template(
        "index.html",
        matches=matches,
        table=table,
        scorers=scorers
    )


if __name__ == "__main__":
    app.run(debug=True)