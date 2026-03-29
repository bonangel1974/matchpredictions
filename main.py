from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

BASE_URL = "https://api.football-data.org/v4"

HEADERS = {
    "X-Auth-Token": API_KEY
}

LEAGUES = {
    "bundesliga": "BL1",
    "seriea": "SA",
    "ligue1": "FL1",
    "championsleague": "CL",
    "worldcup": "WC"
}

TRANSLATIONS = {
    "de": {
        "brand": "MatchPredictions",
        "login": "Login",
        "no_matches": "Keine Spiele verfügbar",
        "upcoming_matches": "Kommende Spiele",
        "league_table": "Tabelle",
        "country_germany": "Deutschland",
        "country_italy": "Italien",
        "country_france": "Frankreich",
        "champions_league": "Champions League",
        "world_cup": "WM",
        "team": "Team",
        "points": "Punkte",
        "position": "#"
    },
    "en": {
        "brand": "MatchPredictions",
        "login": "Login",
        "no_matches": "No matches available",
        "upcoming_matches": "Upcoming Matches",
        "league_table": "Table",
        "country_germany": "Germany",
        "country_italy": "Italy",
        "country_france": "France",
        "champions_league": "Champions League",
        "world_cup": "World Cup",
        "team": "Team",
        "points": "Points",
        "position": "#"
    },
    "it": {
        "brand": "MatchPredictions",
        "login": "Login",
        "no_matches": "Nessuna partita disponibile",
        "upcoming_matches": "Prossime partite",
        "league_table": "Classifica",
        "country_germany": "Germania",
        "country_italy": "Italia",
        "country_france": "Francia",
        "champions_league": "Champions League",
        "world_cup": "Mondiali",
        "team": "Squadra",
        "points": "Punti",
        "position": "#"
    },
    "fr": {
        "brand": "MatchPredictions",
        "login": "Connexion",
        "no_matches": "Aucun match disponible",
        "upcoming_matches": "Matchs à venir",
        "league_table": "Classement",
        "country_germany": "Allemagne",
        "country_italy": "Italie",
        "country_france": "France",
        "champions_league": "Ligue des Champions",
        "world_cup": "Coupe du Monde",
        "team": "Equipe",
        "points": "Points",
        "position": "#"
    }
}


@app.route("/")
def home():
    lang = request.args.get("lang", "de")
    league_key = request.args.get("league", "bundesliga")

    t = TRANSLATIONS.get(lang, TRANSLATIONS["de"])
    league_code = LEAGUES.get(league_key, "BL1")

    matches = []
    table = []
    error = None

    if not API_KEY:
        error = "API_KEY fehlt. Bitte in Render oder lokal als Environment Variable setzen."
        return render_template(
            "index.html",
            t=t,
            lang=lang,
            league=league_key,
            matches=matches,
            table=table,
            error=error
        )

    try:
        # Kommende Spiele
        url_matches = f"{BASE_URL}/competitions/{league_code}/matches?status=SCHEDULED"
        res_matches = requests.get(url_matches, headers=HEADERS, timeout=20)
        res_matches.raise_for_status()
        data_matches = res_matches.json()

        for m in data_matches.get("matches", [])[:8]:
            matches.append({
                "home": m.get("homeTeam", {}).get("name", "Home"),
                "away": m.get("awayTeam", {}).get("name", "Away"),
                "utc_date": m.get("utcDate", ""),
                "matchday": m.get("matchday", "")
            })

        # Tabelle
        url_table = f"{BASE_URL}/competitions/{league_code}/standings"
        res_table = requests.get(url_table, headers=HEADERS, timeout=20)
        res_table.raise_for_status()
        data_table = res_table.json()

        standings = data_table.get("standings", [])

        if standings:
            first_table = standings[0].get("table", [])
            for row in first_table[:10]:
                table.append({
                    "pos": row.get("position", ""),
                    "team": row.get("team", {}).get("name", ""),
                    "points": row.get("points", "")
                })

    except Exception as e:
        error = f"API Fehler: {str(e)}"

    return render_template(
        "index.html",
        t=t,
        lang=lang,
        league=league_key,
        matches=matches,
        table=table,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)