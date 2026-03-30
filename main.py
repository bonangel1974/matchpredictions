from flask import Flask, render_template, request, jsonify
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


def load_matches(league_code: str):
    matches = []

    today = datetime.now(timezone.utc).date()
    future = today + timedelta(days=7)

    res_matches = requests.get(
        f"{BASE_URL}/competitions/{league_code}/matches?dateFrom={today}&dateTo={future}",
        headers=HEADERS,
        timeout=20
    )
    res_matches.raise_for_status()
    data_matches = res_matches.json()

    for m in data_matches.get("matches", [])[:10]:
        home_team = m.get("homeTeam", {})
        away_team = m.get("awayTeam", {})
        score = m.get("score", {})
        full_time = score.get("fullTime", {})
        status = m.get("status", "")

        matches.append({
            "home": home_team.get("name", "Home"),
            "away": away_team.get("name", "Away"),
            "home_logo": find_logo(home_team.get("name", "")),
            "away_logo": find_logo(away_team.get("name", "")),
            "time": format_kickoff(m.get("utcDate", "")),
            "status": status,
            "score_home": full_time.get("home"),
            "score_away": full_time.get("away")
        })

    return matches


def load_table(league_code: str):
    table = []

    res_table = requests.get(
        f"{BASE_URL}/competitions/{league_code}/standings",
        headers=HEADERS,
        timeout=20
    )
    res_table.raise_for_status()
    data_table = res_table.json()

    standings = data_table.get("standings", [])
    if standings:
        for row in standings[0].get("table", [])[:10]:
            team = row.get("team", {})
            team_name = team.get("name", "")
            table.append({
                "pos": row.get("position", ""),
                "team": team_name,
                "logo": find_logo(team_name),
                "points": row.get("points", "")
            })

    return table


def load_scorers(league_code: str):
    scorers = []

    res_scorers = requests.get(
        f"{BASE_URL}/competitions/{league_code}/scorers",
        headers=HEADERS,
        timeout=20
    )
    res_scorers.raise_for_status()
    data_scorers = res_scorers.json()

    for s in data_scorers.get("scorers", [])[:10]:
        team = s.get("team", {})
        team_name = team.get("name", "")
        scorers.append({
            "name": s.get("player", {}).get("name", ""),
            "team": team_name,
            "logo": find_logo(team_name),
            "goals": s.get("goals", 0)
        })

    return scorers


@app.route("/")
def home():
    league_key = request.args.get("league", "bundesliga")
    league_code = LEAGUES.get(league_key, "BL1")

    matches = []
    table = []
    scorers = []
    featured_match = None
    error = None

    try:
        if not API_KEY:
            raise Exception("API_KEY fehlt. Bitte in Render setzen.")

        matches = load_matches(league_code)
        table = load_table(league_code)
        scorers = load_scorers(league_code)

        # Featured Match: zuerst LIVE, sonst erstes Spiel
        if matches:
            live_statuses = {"IN_PLAY", "LIVE", "PAUSED"}

            live_matches = [
                m for m in matches
                if str(m.get("status", "")).upper() in live_statuses
            ]

            if live_matches:
                featured_match = live_matches[0]
            else:
                featured_match = matches[0]

    except Exception as e:
        error = str(e)

    return render_template(
        "index.html",
        matches=matches,
        table=table,
        scorers=scorers,
        featured_match=featured_match,
        error=error,
        league=league_key
    )



@app.route("/api/live-matches")
def api_live_matches():
    league_key = request.args.get("league", "bundesliga")
    league_code = LEAGUES.get(league_key, "BL1")

    try:
        if not API_KEY:
            return jsonify({"success": False, "error": "API_KEY fehlt", "matches": []})

        matches = load_matches(league_code)
        return jsonify({"success": True, "matches": matches})

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "matches": []})


if __name__ == "__main__":
    app.run(debug=True)