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
            "premierleague": "England",
            "seriea": "Italien",
            "ligue1": "Frankreich",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "WM"
        },
        "hero_badge": "Fussball Datenplattform",
        "hero_title": "Moderne Fussball Statistiken mit Premium Look",
        "hero_text": "Kommende Spiele, Tabellen, Top Scorer und spaeter Prognosen, Formkurven und Premium Analysen nach Login.",
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
        "premium_title": "Premium Bereich vorbereiten",
        "premium_text": "Hier kommen später Gewinnwahrscheinlichkeiten, Head-to-Head, Formanalyse, Value Matches und persönliche Favoriten hinein.",
        "premium_button": "Premium ansehen"
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
        "hero_badge": "Football data platform",
        "hero_title": "Modern football statistics with a premium look",
        "hero_text": "Upcoming matches, standings, top scorers and later predictions, form curves and premium analysis after login.",
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
        "premium_title": "Prepare premium area",
        "premium_text": "Later this area will include win probabilities, head-to-head analysis, form analysis, value matches and personal favorites.",
        "premium_button": "View premium"
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
        "hero_badge": "Piattaforma dati calcio",
        "hero_title": "Statistiche calcio moderne con look premium",
        "hero_text": "Prossime partite, classifiche, top marcatori e più avanti pronostici, curve di forma e analisi premium dopo il login.",
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
        "premium_title": "Preparare area premium",
        "premium_text": "Qui arriveranno probabilità di vittoria, testa a testa, analisi della forma, value match e preferiti personali.",
        "premium_button": "Vedi premium"
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
        "hero_badge": "Plateforme de données football",
        "hero_title": "Statistiques football modernes avec look premium",
        "hero_text": "Matchs à venir, classements, meilleurs buteurs et plus tard pronostics, courbes de forme et analyses premium après connexion.",
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
        "premium_title": "Préparer la zone premium",
        "premium_text": "Ici viendront plus tard probabilités de victoire, head-to-head, analyse de forme, value matches et favoris personnels.",
        "premium_button": "Voir premium"
    }
}

TEAM_LOGOS = {
    "Bayern München": "https://logo.clearbit.com/fcbayern.com",
    "FC Bayern München": "https://logo.clearbit.com/fcbayern.com",
    "Bayern Munich": "https://logo.clearbit.com/fcbayern.com",
    "Borussia Dortmund": "https://logo.clearbit.com/bvb.de",
    "Bayer 04 Leverkusen": "https://logo.clearbit.com/bayer04.de",
    "RB Leipzig": "https://logo.clearbit.com/dierotenbullen.com",
    "SC Freiburg": "https://logo.clearbit.com/scfreiburg.com",
    "Eintracht Frankfurt": "https://logo.clearbit.com/eintracht.de",
    "VfB Stuttgart": "https://logo.clearbit.com/vfb.de",
    "TSG Hoffenheim": "https://logo.clearbit.com/tsg-hoffenheim.de",
    "1. FSV Mainz 05": "https://logo.clearbit.com/mainz05.de",
    "VfL Wolfsburg": "https://logo.clearbit.com.vfl-wolfsburg.de",
    "Juventus": "https://logo.clearbit.com/juventus.com",
    "Inter Milan": "https://logo.clearbit.com/inter.it",
    "Inter": "https://logo.clearbit.com/inter.it",
    "AC Milan": "https://logo.clearbit.com/acmilan.com",
    "Milan": "https://logo.clearbit.com/acmilan.com",
    "Roma": "https://logo.clearbit.com/asroma.com",
    "Napoli": "https://logo.clearbit.com/sscnapoli.it",
    "Lazio": "https://logo.clearbit.com.sslazio.it",
    "Atalanta": "https://logo.clearbit.com/atalanta.it",
    "Paris Saint-Germain": "https://logo.clearbit.com/psg.fr",
    "PSG": "https://logo.clearbit.com/psg.fr",
    "Olympique de Marseille": "https://logo.clearbit.com/om.fr",
    "AS Monaco": "https://logo.clearbit.com/asmonaco.com",
    "Lille OSC": "https://logo.clearbit.com/losc.fr",
    "Olympique Lyonnais": "https://logo.clearbit.com/ol.fr",
    "Manchester City": "https://logo.clearbit.com/mancity.com",
    "Manchester United": "https://logo.clearbit.com/manutd.com",
    "Liverpool FC": "https://logo.clearbit.com/liverpoolfc.com",
    "Liverpool": "https://logo.clearbit.com/liverpoolfc.com",
    "Arsenal FC": "https://logo.clearbit.com/arsenal.com",
    "Arsenal": "https://logo.clearbit.com/arsenal.com",
    "Chelsea FC": "https://logo.clearbit.com/chelseafc.com",
    "Chelsea": "https://logo.clearbit.com/chelseafc.com",
    "Tottenham Hotspur": "https://logo.clearbit.com/tottenhamhotspur.com",
    "Real Madrid CF": "https://logo.clearbit.com/realmadrid.com",
    "Real Madrid": "https://logo.clearbit.com/realmadrid.com",
    "FC Barcelona": "https://logo.clearbit.com/fcbarcelona.com",
    "Barcelona": "https://logo.clearbit.com/fcbarcelona.com",
    "Atlético de Madrid": "https://logo.clearbit.com/atleticodemadrid.com",
    "Atlético Madrid": "https://logo.clearbit.com/atleticodemadrid.com",
    "Spain": "https://flagcdn.com/w80/es.png",
    "Germany": "https://flagcdn.com/w80/de.png",
    "France": "https://flagcdn.com/w80/fr.png",
    "Italy": "https://flagcdn.com/w80/it.png",
    "Portugal": "https://flagcdn.com/w80/pt.png",
    "Switzerland": "https://flagcdn.com/w80/ch.png",
    "Austria": "https://flagcdn.com/w80/at.png",
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


@app.route("/login")
def login():
    lang, t = get_translation()
    league = request.args.get("league", "bundesliga")
    return render_template("login.html", t=t, lang=lang, league=league)


@app.route("/register")
def register():
    lang, t = get_translation()
    league = request.args.get("league", "bundesliga")
    return render_template("register.html", t=t, lang=lang, league=league)


@app.route("/premium")
def premium():
    lang, t = get_translation()
    league = request.args.get("league", "bundesliga")
    return render_template("premium.html", t=t, lang=lang, league=league)


if __name__ == "__main__":
    app.run(debug=True)