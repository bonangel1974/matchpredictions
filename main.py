from flask import Flask, render_template, request
import requests

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

TRANSLATIONS = {
    "de": {
        "brand": "MatchPredictions",
        "login": "Login",
        "no_games": "Keine Live Spiele",
        "nav": {
            "bundesliga": "Deutschland",
            "switzerland": "Schweiz",
            "austria": "Österreich",
            "seriea": "Italien",
            "ligue1": "Frankreich",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "WM"
        }
    },
    "en": {
        "brand": "MatchPredictions",
        "login": "Login",
        "no_games": "No live games",
        "nav": {
            "bundesliga": "Germany",
            "switzerland": "Switzerland",
            "austria": "Austria",
            "seriea": "Italy",
            "ligue1": "France",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "World Cup"
        }
    },
    "it": {
        "brand": "MatchPredictions",
        "login": "Login",
        "no_games": "Nessuna partita live",
        "nav": {
            "bundesliga": "Germania",
            "switzerland": "Svizzera",
            "austria": "Austria",
            "seriea": "Italia",
            "ligue1": "Francia",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "Mondiali"
        }
    },
    "fr": {
        "brand": "MatchPredictions",
        "login": "Connexion",
        "no_games": "Aucun match en direct",
        "nav": {
            "bundesliga": "Allemagne",
            "switzerland": "Suisse",
            "austria": "Autriche",
            "seriea": "Italie",
            "ligue1": "France",
            "championsleague": "Ligue des Champions",
            "euro": "EURO",
            "worldcup": "Coupe du Monde"
        }
    }
}


@app.route("/")
def home():
    lang = request.args.get("lang", "de")
    league_key = request.args.get("league", "bundesliga")

    league_id = LEAGUES.get(league_key, 78)
    t = TRANSLATIONS.get(lang, TRANSLATIONS["de"])

    matches = []
    error_message = None

    try:
        headers = {"x-apisports-key": API_KEY}
        url = "https://v3.football.api-sports.io/fixtures?live=all"

        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        data = response.json()

        api_response = data.get("response", [])
        if not isinstance(api_response, list):
            api_response = []

        for m in api_response:
            league = m.get("league", {})
            if league.get("id") == league_id:
                teams = m.get("teams", {})
                home_team = teams.get("home", {})
                away_team = teams.get("away", {})
                goals = m.get("goals", {})
                fixture = m.get("fixture", {})
                status = fixture.get("status", {})

                matches.append({
                    "home": home_team.get("name", "Home"),
                    "away": away_team.get("name", "Away"),
                    "home_logo": home_team.get("logo", ""),
                    "away_logo": away_team.get("logo", ""),
                    "score_home": goals.get("home", 0),
                    "score_away": goals.get("away", 0),
                    "minute": status.get("elapsed", "-")
                })

    except Exception as e:
        error_message = str(e)

    return render_template(
        "index.html",
        matches=matches,
        t=t,
        lang=lang,
        league=league_key,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)