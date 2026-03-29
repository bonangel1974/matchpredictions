from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "DEIN_API_KEY"

# Ligen Europa + International
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

    headers = {"x-apisports-key": API_KEY}

    url = "https://v3.football.api-sports.io/fixtures?live=all"
    response = requests.get(url, headers=headers)
    data = response.json()

    matches = []

    for m in data["response"]:
        if m["league"]["id"] == league_id:

            matches.append({
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "home_logo": m["teams"]["home"]["logo"],
                "away_logo": m["teams"]["away"]["logo"],
                "score_home": m["goals"]["home"],
                "score_away": m["goals"]["away"],
                "minute": m["fixture"]["status"]["elapsed"]
            })

    return render_template(
        "index.html",
        matches=matches,
        t=t,
        lang=lang,
        league=league_key
    )


if __name__ == "__main__":
    app.run(debug=True)