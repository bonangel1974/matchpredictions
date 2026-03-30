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

TRANSLATIONS = {
    "de": {
        "brand": "MatchPredictions",
        "login": "Login",
        "nav": {
            "bundesliga": "Deutschland",
            "switzerland": "Schweiz",
            "austria": "Österreich",
            "premierleague": "England",
            "seriea": "Italien",
            "ligue1": "Frankreich",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "WM"
        },
        "hero_badge": "Europäische Fussball Plattform",
        "hero_title": "Fussball Statistiken für Europa",
        "hero_text": "Deutschland, Schweiz, Österreich, England, Italien, Frankreich sowie Champions League, EURO und WM direkt auf der Hauptseite.",
        "featured_match": "Featured Match",
        "next_days": "Nächste 7 Tage",
        "matches_title": "Kommende Spiele",
        "table_title": "Tabelle",
        "scorers_title": "Top Scorer",
        "table_badge": "Top 10",
        "scorers_badge": "Top 10",
        "position": "#",
        "team": "Team",
        "points": "Punkte",
        "goals": "Tore",
        "empty_matches": "Keine Spiele im gewählten Zeitraum verfügbar.",
        "empty_table": "Keine Tabelle verfügbar.",
        "empty_scorers": "Keine Torschützen verfügbar.",
        "premium_title": "Mehr Analysen nach Login",
        "premium_text": "Später mit Wahrscheinlichkeiten, Formanalyse, Head-to-Head und weiteren Premium Funktionen.",
        "premium_button": "Premium ansehen"
    },
    "en": {
        "brand": "MatchPredictions",
        "login": "Login",
        "nav": {
            "bundesliga": "Germany",
            "switzerland": "Switzerland",
            "austria": "Austria",
            "premierleague": "England",
            "seriea": "Italy",
            "ligue1": "France",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "World Cup"
        },
        "hero_badge": "European football platform",
        "hero_title": "Football statistics for Europe",
        "hero_text": "Germany, Switzerland, Austria, England, Italy, France plus Champions League, EURO and World Cup directly on the homepage.",
        "featured_match": "Featured Match",
        "next_days": "Next 7 Days",
        "matches_title": "Upcoming Matches",
        "table_title": "Table",
        "scorers_title": "Top Scorers",
        "table_badge": "Top 10",
        "scorers_badge": "Top 10",
        "position": "#",
        "team": "Team",
        "points": "Points",
        "goals": "Goals",
        "empty_matches": "No matches available in the selected period.",
        "empty_table": "No table available.",
        "empty_scorers": "No scorers available.",
        "premium_title": "More analysis after login",
        "premium_text": "Later with probabilities, form analysis, head-to-head and more premium features.",
        "premium_button": "View premium"
    },
    "it": {
        "brand": "MatchPredictions",
        "login": "Login",
        "nav": {
            "bundesliga": "Germania",
            "switzerland": "Svizzera",
            "austria": "Austria",
            "premierleague": "Inghilterra",
            "seriea": "Italia",
            "ligue1": "Francia",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "Mondiali"
        },
        "hero_badge": "Piattaforma europea di calcio",
        "hero_title": "Statistiche calcio per Europa",
        "hero_text": "Germania, Svizzera, Austria, Inghilterra, Italia, Francia più Champions League, EURO e Mondiali direttamente nella homepage.",
        "featured_match": "Partita in evidenza",
        "next_days": "Prossimi 7 giorni",
        "matches_title": "Prossime Partite",
        "table_title": "Classifica",
        "scorers_title": "Top Marcatori",
        "table_badge": "Top 10",
        "scorers_badge": "Top 10",
        "position": "#",
        "team": "Squadra",
        "points": "Punti",
        "goals": "Gol",
        "empty_matches": "Nessuna partita disponibile nel periodo selezionato.",
        "empty_table": "Nessuna classifica disponibile.",
        "empty_scorers": "Nessun marcatore disponibile.",
        "premium_title": "Più analisi dopo il login",
        "premium_text": "Più avanti con probabilità, analisi della forma, head-to-head e altre funzioni premium.",
        "premium_button": "Vedi premium"
    },
    "fr": {
        "brand": "MatchPredictions",
        "login": "Connexion",
        "nav": {
            "bundesliga": "Allemagne",
            "switzerland": "Suisse",
            "austria": "Autriche",
            "premierleague": "Angleterre",
            "seriea": "Italie",
            "ligue1": "France",
            "championsleague": "Ligue des Champions",
            "euro": "EURO",
            "worldcup": "Coupe du Monde"
        },
        "hero_badge": "Plateforme européenne de football",
        "hero_title": "Statistiques football pour Europe",
        "hero_text": "Allemagne, Suisse, Autriche, Angleterre, Italie, France ainsi que Ligue des Champions, EURO et Coupe du Monde directement sur la page principale.",
        "featured_match": "Match vedette",
        "next_days": "7 prochains jours",
        "matches_title": "Matchs à venir",
        "table_title": "Classement",
        "scorers_title": "Top Buteurs",
        "table_badge": "Top 10",
        "scorers_badge": "Top 10",
        "position": "#",
        "team": "Equipe",
        "points": "Points",
        "goals": "Buts",
        "empty_matches": "Aucun match disponible pour la période sélectionnée.",
        "empty_table": "Aucun classement disponible.",
        "empty_scorers": "Aucun buteur disponible.",
        "premium_title": "Plus d analyses après connexion",
        "premium_text": "Plus tard avec probabilités, analyse de forme, head-to-head et autres fonctions premium.",
        "premium_button": "Voir premium"
    }
}


def format_kickoff(utc_value: str) -> str:
    if not utc_value:
        return "-"
    try:
        dt = datetime.fromisoformat(utc_value.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return utc_value


def get_translation():
    lang = request.args.get("lang", "de")
    t = TRANSLATIONS.get(lang, TRANSLATIONS["de"])
    return lang, t


@app.route("/")
def home():
    lang, t = get_translation()
    league_key = request.args.get("league", "bundesliga")
    league_code = LEAGUES.get(league_key, "BL1")

    matches = []
    table = []
    scorers = []
    featured_match = None
    error = None

    if not API_KEY:
        error = "API_KEY fehlt. Bitte in Render als Environment Variable setzen."
        return render_template(
            "index.html",
            t=t,
            lang=lang,
            league=league_key,
            matches=matches,
            table=table,
            scorers=scorers,
            featured_match=featured_match,
            error=error
        )

    try:
        today = datetime.now(timezone.utc).date()
        future = today + timedelta(days=7)

        res_matches = requests.get(
            f"{BASE_URL}/competitions/{league_code}/matches?dateFrom={today}&dateTo={future}",
            headers=HEADERS,
            timeout=20
        )
        res_matches.raise_for_status()
        data_matches = res_matches.json()

        for m in data_matches.get("matches", [])[:8]:
            home_team = m.get("homeTeam", {})
            away_team = m.get("awayTeam", {})
            score = m.get("score", {})
            full_time = score.get("fullTime", {})

            match_obj = {
                "home": home_team.get("name", "Home"),
                "away": away_team.get("name", "Away"),
                "home_short": home_team.get("shortName") or home_team.get("tla") or home_team.get("name", "Home"),
                "away_short": away_team.get("shortName") or away_team.get("tla") or away_team.get("name", "Away"),
                "home_logo": find_logo(home_team.get("name", "")),
                "away_logo": find_logo(away_team.get("name", "")),
                "kickoff": format_kickoff(m.get("utcDate", "")),
                "status": m.get("status", ""),
                "score_home": full_time.get("home"),
                "score_away": full_time.get("away"),
                "matchday": m.get("matchday", "")
            }
            matches.append(match_obj)

        if matches:
            featured_match = matches[0]

        res_table = requests.get(
            f"{BASE_URL}/competitions/{league_code}/standings",
            headers=HEADERS,
            timeout=20
        )
        res_table.raise_for_status()
        data_table = res_table.json()

        standings = data_table.get("standings", [])
        if standings:
            first_table = standings[0].get("table", [])
            for row in first_table[:10]:
                team = row.get("team", {})
                team_name = team.get("name", "")
                table.append({
                    "pos": row.get("position", ""),
                    "team": team_name,
                    "logo": find_logo(team_name),
                    "points": row.get("points", ""),
                    "goal_diff": row.get("goalDifference", "")
                })

        res_scorers = requests.get(
            f"{BASE_URL}/competitions/{league_code}/scorers",
            headers=HEADERS,
            timeout=20
        )
        res_scorers.raise_for_status()
        data_scorers = res_scorers.json()

        for s in data_scorers.get("scorers", [])[:10]:
            player = s.get("player", {})
            team = s.get("team", {})
            team_name = team.get("name", "")
            scorers.append({
                "name": player.get("name", ""),
                "team": team_name,
                "team_logo": find_logo(team_name),
                "goals": s.get("goals", 0)
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
        scorers=scorers,
        featured_match=featured_match,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)