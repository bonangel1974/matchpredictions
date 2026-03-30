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
        "register": "Registrieren",
        "premium": "Premium",
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
        "register": "Register",
        "premium": "Premium",
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
        "register": "Registrati",
        "premium": "Premium",
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
        "register": "Inscription",
        "premium": "Premium",
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

TEAM_LOGOS = {
    "Bayern München": "https://logo.clearbit.com/fcbayern.com",
    "FC Bayern München": "https://logo.clearbit.com/fcbayern.com",
    "Bayern Munich": "https://logo.clearbit.com/fcbayern.com",
    "Borussia Dortmund": "https://logo.clearbit.com/bvb.de",
    "Bayer 04 Leverkusen": "https://logo.clearbit.com/bayer04.de",
    "RB Leipzig": "https://logo.clearbit.com/redbullsalzburg.at",
    "Juventus": "https://logo.clearbit.com/juventus.com",
    "Inter": "https://logo.clearbit.com/inter.it",
    "Inter Milan": "https://logo.clearbit.com/inter.it",
    "AC Milan": "https://logo.clearbit.com/acmilan.com",
    "Milan": "https://logo.clearbit.com/acmilan.com",
    "Napoli": "https://logo.clearbit.com/sscnapoli.it",
    "Roma": "https://logo.clearbit.com/asroma.com",
    "Paris Saint-Germain": "https://logo.clearbit.com/psg.fr",
    "PSG": "https://logo.clearbit.com/psg.fr",
    "Olympique de Marseille": "https://logo.clearbit.com/om.fr",
    "AS Monaco": "https://logo.clearbit.com/asmonaco.com",
    "Manchester City": "https://logo.clearbit.com/mancity.com",
    "Manchester United": "https://logo.clearbit.com/manutd.com",
    "Arsenal": "https://logo.clearbit.com/arsenal.com",
    "Arsenal FC": "https://logo.clearbit.com/arsenal.com",
    "Chelsea": "https://logo.clearbit.com/chelseafc.com",
    "Chelsea FC": "https://logo.clearbit.com/chelseafc.com",
    "Liverpool": "https://logo.clearbit.com/liverpoolfc.com",
    "Liverpool FC": "https://logo.clearbit.com/liverpoolfc.com",
    "FC Basel 1893": "https://logo.clearbit.com/fcb.ch",
    "BSC Young Boys": "https://logo.clearbit.com/bscyb.ch",
    "FC Zürich": "https://logo.clearbit.com/fcz.ch",
    "Servette FC": "https://logo.clearbit.com/servettefc.ch",
    "FC Lugano": "https://logo.clearbit.com/fclugano.com",
    "FC St. Gallen 1879": "https://logo.clearbit.com/fcsg.ch",
    "SK Rapid Wien": "https://logo.clearbit.com/skrapid.at",
    "FK Austria Wien": "https://logo.clearbit.com/fk-austria.at",
    "FC Red Bull Salzburg": "https://logo.clearbit.com/redbullsalzburg.at",
    "LASK": "https://logo.clearbit.com/lask.at",
    "Sturm Graz": "https://logo.clearbit.com/sksturm.at",
    "Germany": "https://flagcdn.com/w80/de.png",
    "Switzerland": "https://flagcdn.com/w80/ch.png",
    "Austria": "https://flagcdn.com/w80/at.png",
    "France": "https://flagcdn.com/w80/fr.png",
    "Italy": "https://flagcdn.com/w80/it.png",
    "England": "https://flagcdn.com/w80/gb-eng.png"
}


def get_logo(team_name: str) -> str:
    return TEAM_LOGOS.get(team_name, "https://placehold.co/80x80/1f2a44/ffffff?text=%20")


def format_kickoff(utc_value: str) -> str:
    if not utc_value:
        return "-"
    try:
        dt = datetime.fromisoformat(utc_value.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M UTC")
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

        url_matches = f"{BASE_URL}/competitions/{league_code}/matches?dateFrom={today}&dateTo={future}"
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
                "home_logo": get_logo(home_team.get("name", "")),
                "away_logo": get_logo(away_team.get("name", "")),
                "kickoff": format_kickoff(m.get("utcDate", "")),
                "status": m.get("status", ""),
                "score_home": full_time.get("home"),
                "score_away": full_time.get("away"),
                "matchday": m.get("matchday", "")
            }
            matches.append(match_obj)

        if matches:
            featured_match = matches[0]

        url_table = f"{BASE_URL}/competitions/{league_code}/standings"
        res_table = requests.get(url_table, headers=HEADERS, timeout=20)
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
                    "logo": get_logo(team_name),
                    "points": row.get("points", ""),
                    "goal_diff": row.get("goalDifference", "")
                })

        url_scorers = f"{BASE_URL}/competitions/{league_code}/scorers"
        res_scorers = requests.get(url_scorers, headers=HEADERS, timeout=20)
        res_scorers.raise_for_status()
        data_scorers = res_scorers.json()

        for s in data_scorers.get("scorers", [])[:10]:
            player = s.get("player", {})
            team = s.get("team", {})
            team_name = team.get("name", "")
            scorers.append({
                "name": player.get("name", ""),
                "team": team_name,
                "team_logo": get_logo(team_name),
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