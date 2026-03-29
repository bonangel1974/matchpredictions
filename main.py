from flask import Flask, render_template, request
import requests
import os
from datetime import datetime, timedelta, timezone

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
    "worldcup": "WC",
    "euro": "EC",
    "premierleague": "PL"
}

TRANSLATIONS = {
    "de": {
        "brand": "MatchPredictions",
        "login": "Login",
        "nav": {
            "bundesliga": "Deutschland",
            "premierleague": "England",
            "seriea": "Italien",
            "ligue1": "Frankreich",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "WM"
        },
        "hero_title": "Fussball Statistiken mit Vertrauen",
        "hero_text": "Live Spiele, kommende Partien, Tabellen und Top Scorer. Premium Analysen, Prognosen und Wahrscheinlichkeiten spaeter nach Login.",
        "matches_title": "Kommende Spiele",
        "table_title": "Tabelle",
        "scorers_title": "Top Scorer",
        "empty_matches": "Keine Spiele im gewählten Zeitraum verfügbar.",
        "empty_table": "Keine Tabelle verfügbar.",
        "empty_scorers": "Keine Torschützen verfügbar.",
        "position": "#",
        "team": "Team",
        "points": "Punkte",
        "goals": "Tore",
        "featured_match": "Featured Match",
        "next_days": "Nächste 7 Tage",
        "top_scorers_badge": "Top 10",
        "table_badge": "Live Stand",
        "premium_box_title": "Mehr Analysen nach Login",
        "premium_box_text": "Spaeter mit Gewinnwahrscheinlichkeiten, Head-to-Head, Formanalyse und weiteren Premium Features.",
        "premium_button": "Mehr erfahren"
    },
    "en": {
        "brand": "MatchPredictions",
        "login": "Login",
        "nav": {
            "bundesliga": "Germany",
            "premierleague": "England",
            "seriea": "Italy",
            "ligue1": "France",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "World Cup"
        },
        "hero_title": "Football statistics with trust",
        "hero_text": "Live matches, upcoming fixtures, standings and top scorers. Premium analysis, predictions and probabilities later after login.",
        "matches_title": "Upcoming Matches",
        "table_title": "Table",
        "scorers_title": "Top Scorers",
        "empty_matches": "No matches available in the selected period.",
        "empty_table": "No table available.",
        "empty_scorers": "No scorers available.",
        "position": "#",
        "team": "Team",
        "points": "Points",
        "goals": "Goals",
        "featured_match": "Featured Match",
        "next_days": "Next 7 Days",
        "top_scorers_badge": "Top 10",
        "table_badge": "Live Table",
        "premium_box_title": "More analysis after login",
        "premium_box_text": "Later with win probabilities, head-to-head, form analysis and more premium features.",
        "premium_button": "Learn more"
    },
    "it": {
        "brand": "MatchPredictions",
        "login": "Login",
        "nav": {
            "bundesliga": "Germania",
            "premierleague": "Inghilterra",
            "seriea": "Italia",
            "ligue1": "Francia",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "Mondiali"
        },
        "hero_title": "Statistiche calcio con fiducia",
        "hero_text": "Partite live, prossimi incontri, classifiche e migliori marcatori. Analisi premium, pronostici e probabilità più avanti dopo il login.",
        "matches_title": "Prossime Partite",
        "table_title": "Classifica",
        "scorers_title": "Top Marcatori",
        "empty_matches": "Nessuna partita disponibile nel periodo selezionato.",
        "empty_table": "Nessuna classifica disponibile.",
        "empty_scorers": "Nessun marcatore disponibile.",
        "position": "#",
        "team": "Squadra",
        "points": "Punti",
        "goals": "Gol",
        "featured_match": "Partita in evidenza",
        "next_days": "Prossimi 7 giorni",
        "top_scorers_badge": "Top 10",
        "table_badge": "Classifica Live",
        "premium_box_title": "Più analisi dopo il login",
        "premium_box_text": "Più avanti con probabilità di vittoria, testa a testa, analisi della forma e altre funzioni premium.",
        "premium_button": "Scopri di più"
    },
    "fr": {
        "brand": "MatchPredictions",
        "login": "Connexion",
        "nav": {
            "bundesliga": "Allemagne",
            "premierleague": "Angleterre",
            "seriea": "Italie",
            "ligue1": "France",
            "championsleague": "Ligue des Champions",
            "euro": "EURO",
            "worldcup": "Coupe du Monde"
        },
        "hero_title": "Statistiques football avec confiance",
        "hero_text": "Matchs en direct, rencontres à venir, classements et meilleurs buteurs. Analyses premium, pronostics et probabilités plus tard après connexion.",
        "matches_title": "Matchs à venir",
        "table_title": "Classement",
        "scorers_title": "Top Buteurs",
        "empty_matches": "Aucun match disponible pour la période sélectionnée.",
        "empty_table": "Aucun classement disponible.",
        "empty_scorers": "Aucun buteur disponible.",
        "position": "#",
        "team": "Equipe",
        "points": "Points",
        "goals": "Buts",
        "featured_match": "Match vedette",
        "next_days": "7 prochains jours",
        "top_scorers_badge": "Top 10",
        "table_badge": "Classement Live",
        "premium_box_title": "Plus d analyses après connexion",
        "premium_box_text": "Plus tard avec probabilités de victoire, head-to-head, analyse de forme et autres fonctions premium.",
        "premium_button": "En savoir plus"
    }
}


def format_kickoff(utc_value: str) -> str:
    if not utc_value:
        return "-"
    try:
        dt = datetime.fromisoformat(utc_value.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M UTC")
    except Exception:
        return utc_value


@app.route("/")
def home():
    lang = request.args.get("lang", "de")
    league_key = request.args.get("league", "bundesliga")

    t = TRANSLATIONS.get(lang, TRANSLATIONS["de"])
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

        # Spiele
        url_matches = (
            f"{BASE_URL}/competitions/{league_code}/matches"
            f"?dateFrom={today}&dateTo={future}"
        )
        res_matches = requests.get(url_matches, headers=HEADERS, timeout=20)
        res_matches.raise_for_status()
        data_matches = res_matches.json()

        all_matches = data_matches.get("matches", [])

        for m in all_matches[:8]:
            home_team = m.get("homeTeam", {})
            away_team = m.get("awayTeam", {})
            score = m.get("score", {})
            full_time = score.get("fullTime", {})

            match_obj = {
                "home": home_team.get("name", "Home"),
                "away": away_team.get("name", "Away"),
                "home_short": home_team.get("shortName") or home_team.get("tla") or home_team.get("name", "Home"),
                "away_short": away_team.get("shortName") or away_team.get("tla") or away_team.get("name", "Away"),
                "kickoff": format_kickoff(m.get("utcDate", "")),
                "status": m.get("status", ""),
                "score_home": full_time.get("home"),
                "score_away": full_time.get("away"),
                "matchday": m.get("matchday", "")
            }
            matches.append(match_obj)

        if matches:
            featured_match = matches[0]

        # Tabelle
        url_table = f"{BASE_URL}/competitions/{league_code}/standings"
        res_table = requests.get(url_table, headers=HEADERS, timeout=20)
        res_table.raise_for_status()
        data_table = res_table.json()

        standings = data_table.get("standings", [])
        if standings:
            first_table = standings[0].get("table", [])
            for row in first_table[:10]:
                team = row.get("team", {})
                table.append({
                    "pos": row.get("position", ""),
                    "team": team.get("name", ""),
                    "short": team.get("shortName") or team.get("tla") or team.get("name", ""),
                    "points": row.get("points", ""),
                    "goal_diff": row.get("goalDifference", "")
                })

        # Top Scorer
        url_scorers = f"{BASE_URL}/competitions/{league_code}/scorers"
        res_scorers = requests.get(url_scorers, headers=HEADERS, timeout=20)
        res_scorers.raise_for_status()
        data_scorers = res_scorers.json()

        for s in data_scorers.get("scorers", [])[:10]:
            player = s.get("player", {})
            team = s.get("team", {})
            scorers.append({
                "name": player.get("name", ""),
                "team": team.get("name", ""),
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