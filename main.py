from flask import Flask, render_template, request, jsonify, make_response
import requests
import os
from datetime import datetime, timedelta, timezone
from team_logos import find_logo

app = Flask(__name__)

# =========================================================
# API KEYS / URLS
# =========================================================
API_KEY = os.environ.get("API_KEY")  # football-data.org
API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY")  # api-football

BASE_URL_FD = "https://api.football-data.org/v4"
BASE_URL_API2 = "https://v3.football.api-sports.io"

HEADERS_FD = {
    "X-Auth-Token": API_KEY
}

HEADERS_API2 = {
    "x-apisports-key": API_FOOTBALL_KEY
}

CURRENT_SEASON = int(os.environ.get("FOOTBALL_SEASON", "2024"))

# =========================================================
# LIGEN
# football-data = alles Kostenlose / Gute
# api-football = fehlende Länder
# Die api-football IDs bitte bei Bedarf im Dashboard prüfen
# =========================================================
LEAGUES = {
    # football-data
    "bundesliga": "BL1",
    "premierleague": "PL",
    "seriea": "SA",
    "ligue1": "FL1",
    "laliga": "PD",
    "championsleague": "CL",
    "euro": "EC",
    "worldcup": "WC",
    "eredivisie": "DED",
    "primeiraliga": "PPL",
    "championship": "ELC",
    "brazil": "BSA",

    # api-football
    "switzerland": 207,
    "austria": 218,
    "turkey": 203,
    "hungary": 271,
    "albania": 302
}

LEAGUE_PROVIDERS = {
    "bundesliga": "fd",
    "premierleague": "fd",
    "seriea": "fd",
    "ligue1": "fd",
    "laliga": "fd",
    "championsleague": "fd",
    "euro": "fd",
    "worldcup": "fd",
    "eredivisie": "fd",
    "primeiraliga": "fd",
    "championship": "fd",
    "brazil": "fd",

    "switzerland": "api2",
    "austria": "api2",
    "turkey": "api2",
    "hungary": "api2",
    "albania": "api2"
}

# =========================================================
# STANDARD
# =========================================================
DEFAULT_PREFS = {
    "league": "bundesliga",
    "lang": "de"
}

COUNTRY_DEFAULTS = {
    "CH": {"league": "switzerland", "lang": "de"},
    "DE": {"league": "bundesliga", "lang": "de"},
    "AT": {"league": "austria", "lang": "de"},
    "IT": {"league": "seriea", "lang": "it"},
    "FR": {"league": "ligue1", "lang": "fr"},
    "GB": {"league": "premierleague", "lang": "en"},
    "ES": {"league": "laliga", "lang": "en"},
    "NL": {"league": "eredivisie", "lang": "en"},
    "PT": {"league": "primeiraliga", "lang": "en"},
    "BR": {"league": "brazil", "lang": "en"},
    "TR": {"league": "turkey", "lang": "en"},
    "HU": {"league": "hungary", "lang": "en"},
    "AL": {"league": "albania", "lang": "en"},
}

# =========================================================
# ÜBERSETZUNGEN
# Muss zu base.html + index.html passen
# =========================================================
TRANSLATIONS = {
    "de": {
        "brand": "MatchPredictions",
        "nav_germany": "Deutschland",
        "nav_switzerland": "Schweiz",
        "nav_austria": "Österreich",
        "nav_england": "England",
        "nav_italy": "Italien",
        "nav_france": "Frankreich",
        "nav_europe": "Europa",
        "live": "Live",
        "login": "Login",
        "premium": "Premium",
        "hero_kicker": "AI Match Predictions",
        "hero_title_line1": "AI Match Predictions",
        "hero_title_line2": "für Europa",
        "hero_subtitle": "Daten. Trends. Gewinnstrategien.",
        "hero_btn_predictions": "Vorhersagen ansehen",
        "hero_btn_trial": "Kostenlos testen",
        "ai_analysis": "AI Analyse",
        "premium_badge": "PREMIUM",
        "form_analysis": "Form Analyse",
        "head_to_head": "Head-to-Head",
        "goal_trend": "Goal Trend",
        "injury_impact": "Injury Impact",
        "result": "Ergebnis:",
        "premium_only": "Nur für Premium",
        "premium_after_sub": "Prediction nach Abo sichtbar",
        "premium_feature": "Premium Feature",
        "top_matches": "Top Matches",
        "top_matches_sub": "Heute wichtigste Spiele und Vorhersagen",
        "prediction": "Prediction",
        "confidence": "Confidence",
        "details": "Details",
        "tip": "Tipp",
        "tip_premium_only": "Nur für Premium",
        "unlock_premium": "Premium freischalten",
        "prediction_premium_only": "Prediction nur für Premium",
        "prediction_locked_text": "Vorhersagen, Confidence und Tipps werden nach Abo-Freischaltung angezeigt.",
        "live_in_play": "Live und In-Play",
        "live_in_play_sub": "Echtzeit Vorhersagen und Updates",
        "live_prediction": "Live Prediction",
        "subscription": "Abo",
        "league": "League",
        "table": "Tabelle",
        "players": "Players",
        "top_scorer": "Top Scorer",
        "upgrade_premium": "Upgrade auf Premium",
        "unlimited_predictions": "Unlimitierte Vorhersagen",
        "ai_analysis_full": "AI Analysen",
        "live_insights": "Live Insights",
        "early_access": "Early Access",
        "unlock_now": "Jetzt freischalten",
        "top_teams_today": "Top Teams heute",
        "hot": "Hot",
        "cold": "Cold",
        "to_live_area": "Zum Live-Bereich",
        "footer_text": "AI-gestützte Fussballvorhersagen für Europas Top Ligen.",
        "navigation": "Navigation",
        "matches": "Matches",
        "predictions": "Predictions",
        "stats": "Stats",
        "legal": "Rechtliches",
        "imprint": "Impressum",
        "privacy": "Datenschutz",
        "terms": "AGB",
        "stay_updated": "Stay Updated",
        "newsletter_text": "Erhalte die besten Vorhersagen per E-Mail.",
        "email_placeholder": "Deine E-Mail",
        "subscribe": "Abonnieren",
        "points": "Punkte",
        "draw": "Unentschieden",
        "home_win": "Heimsieg",
        "over_goals": "Über 2.5 Tore",
        "under_goals": "Unter 3.5 Tore",
        "all_rights_reserved": "Alle Rechte vorbehalten."
    },
    "en": {
        "brand": "MatchPredictions",
        "nav_germany": "Germany",
        "nav_switzerland": "Switzerland",
        "nav_austria": "Austria",
        "nav_england": "England",
        "nav_italy": "Italy",
        "nav_france": "France",
        "nav_europe": "Europe",
        "live": "Live",
        "login": "Login",
        "premium": "Premium",
        "hero_kicker": "AI Match Predictions",
        "hero_title_line1": "AI Match Predictions",
        "hero_title_line2": "for Europe",
        "hero_subtitle": "Data. Trends. Winning strategies.",
        "hero_btn_predictions": "View predictions",
        "hero_btn_trial": "Try for free",
        "ai_analysis": "AI Analysis",
        "premium_badge": "PREMIUM",
        "form_analysis": "Form analysis",
        "head_to_head": "Head-to-Head",
        "goal_trend": "Goal trend",
        "injury_impact": "Injury impact",
        "result": "Result:",
        "premium_only": "Premium only",
        "premium_after_sub": "Prediction visible after subscription",
        "premium_feature": "Premium feature",
        "top_matches": "Top Matches",
        "top_matches_sub": "Today's biggest matches and predictions",
        "prediction": "Prediction",
        "confidence": "Confidence",
        "details": "Details",
        "tip": "Tip",
        "tip_premium_only": "Premium only",
        "unlock_premium": "Unlock premium",
        "prediction_premium_only": "Prediction only for premium",
        "prediction_locked_text": "Predictions, confidence and tips are shown after premium activation.",
        "live_in_play": "Live and In-Play",
        "live_in_play_sub": "Real-time predictions and updates",
        "live_prediction": "Live Prediction",
        "subscription": "Subscription",
        "league": "League",
        "table": "Table",
        "players": "Players",
        "top_scorer": "Top Scorer",
        "upgrade_premium": "Upgrade to premium",
        "unlimited_predictions": "Unlimited predictions",
        "ai_analysis_full": "AI analysis",
        "live_insights": "Live insights",
        "early_access": "Early access",
        "unlock_now": "Unlock now",
        "top_teams_today": "Top teams today",
        "hot": "Hot",
        "cold": "Cold",
        "to_live_area": "Go to live area",
        "footer_text": "AI-powered football predictions for Europe's top leagues.",
        "navigation": "Navigation",
        "matches": "Matches",
        "predictions": "Predictions",
        "stats": "Stats",
        "legal": "Legal",
        "imprint": "Imprint",
        "privacy": "Privacy",
        "terms": "Terms",
        "stay_updated": "Stay Updated",
        "newsletter_text": "Get the best predictions by email.",
        "email_placeholder": "Your email",
        "subscribe": "Subscribe",
        "points": "Points",
        "draw": "Draw",
        "home_win": "Home Win",
        "over_goals": "Over 2.5 Goals",
        "under_goals": "Under 3.5 Goals",
        "all_rights_reserved": "All rights reserved."
    },
    "fr": {
        "brand": "MatchPredictions",
        "nav_germany": "Allemagne",
        "nav_switzerland": "Suisse",
        "nav_austria": "Autriche",
        "nav_england": "Angleterre",
        "nav_italy": "Italie",
        "nav_france": "France",
        "nav_europe": "Europe",
        "live": "Live",
        "login": "Connexion",
        "premium": "Premium",
        "hero_kicker": "AI Match Predictions",
        "hero_title_line1": "AI Match Predictions",
        "hero_title_line2": "pour l'Europe",
        "hero_subtitle": "Données. Tendances. Stratégies gagnantes.",
        "hero_btn_predictions": "Voir les prédictions",
        "hero_btn_trial": "Essayer gratuitement",
        "ai_analysis": "Analyse AI",
        "premium_badge": "PREMIUM",
        "form_analysis": "Analyse de forme",
        "head_to_head": "Head-to-Head",
        "goal_trend": "Tendance des buts",
        "injury_impact": "Impact des blessures",
        "result": "Résultat :",
        "premium_only": "Seulement premium",
        "premium_after_sub": "Prédiction visible après abonnement",
        "premium_feature": "Fonction premium",
        "top_matches": "Top Matches",
        "top_matches_sub": "Les matchs et prédictions les plus importants aujourd'hui",
        "prediction": "Prédiction",
        "confidence": "Confiance",
        "details": "Détails",
        "tip": "Conseil",
        "tip_premium_only": "Seulement premium",
        "unlock_premium": "Activer premium",
        "prediction_premium_only": "Prédiction réservée au premium",
        "prediction_locked_text": "Les prédictions, la confiance et les conseils sont visibles après activation premium.",
        "live_in_play": "Live et In-Play",
        "live_in_play_sub": "Prédictions et mises à jour en temps réel",
        "live_prediction": "Prédiction live",
        "subscription": "Abonnement",
        "league": "League",
        "table": "Classement",
        "players": "Joueurs",
        "top_scorer": "Top Buteurs",
        "upgrade_premium": "Passer au premium",
        "unlimited_predictions": "Prédictions illimitées",
        "ai_analysis_full": "Analyses AI",
        "live_insights": "Insights live",
        "early_access": "Accès anticipé",
        "unlock_now": "Activer maintenant",
        "top_teams_today": "Top équipes du jour",
        "hot": "Hot",
        "cold": "Cold",
        "to_live_area": "Vers la zone live",
        "footer_text": "Prédictions football assistées par AI pour les meilleures ligues d'Europe.",
        "navigation": "Navigation",
        "matches": "Matches",
        "predictions": "Predictions",
        "stats": "Stats",
        "legal": "Mentions légales",
        "imprint": "Impressum",
        "privacy": "Confidentialité",
        "terms": "CGU",
        "stay_updated": "Stay Updated",
        "newsletter_text": "Recevez les meilleures prédictions par e-mail.",
        "email_placeholder": "Votre e-mail",
        "subscribe": "S'abonner",
        "points": "Points",
        "draw": "Match nul",
        "home_win": "Victoire à domicile",
        "over_goals": "Plus de 2.5 buts",
        "under_goals": "Moins de 3.5 buts",
        "all_rights_reserved": "Tous droits réservés."
    },
    "it": {
        "brand": "MatchPredictions",
        "nav_germany": "Germania",
        "nav_switzerland": "Svizzera",
        "nav_austria": "Austria",
        "nav_england": "Inghilterra",
        "nav_italy": "Italia",
        "nav_france": "Francia",
        "nav_europe": "Europa",
        "live": "Live",
        "login": "Login",
        "premium": "Premium",
        "hero_kicker": "AI Match Predictions",
        "hero_title_line1": "AI Match Predictions",
        "hero_title_line2": "per l'Europa",
        "hero_subtitle": "Dati. Tendenze. Strategie vincenti.",
        "hero_btn_predictions": "Vedi previsioni",
        "hero_btn_trial": "Prova gratis",
        "ai_analysis": "Analisi AI",
        "premium_badge": "PREMIUM",
        "form_analysis": "Analisi forma",
        "head_to_head": "Head-to-Head",
        "goal_trend": "Trend gol",
        "injury_impact": "Impatto infortuni",
        "result": "Risultato:",
        "premium_only": "Solo premium",
        "premium_after_sub": "Previsione visibile dopo abbonamento",
        "premium_feature": "Funzione premium",
        "top_matches": "Top Matches",
        "top_matches_sub": "Le partite e previsioni più importanti di oggi",
        "prediction": "Previsione",
        "confidence": "Confidenza",
        "details": "Dettagli",
        "tip": "Suggerimento",
        "tip_premium_only": "Solo premium",
        "unlock_premium": "Sblocca premium",
        "prediction_premium_only": "Previsione solo per premium",
        "prediction_locked_text": "Previsioni, confidenza e suggerimenti sono visibili dopo l'attivazione premium.",
        "live_in_play": "Live e In-Play",
        "live_in_play_sub": "Previsioni e aggiornamenti in tempo reale",
        "live_prediction": "Previsione live",
        "subscription": "Abbonamento",
        "league": "League",
        "table": "Classifica",
        "players": "Giocatori",
        "top_scorer": "Top Marcatori",
        "upgrade_premium": "Passa al premium",
        "unlimited_predictions": "Previsioni illimitate",
        "ai_analysis_full": "Analisi AI",
        "live_insights": "Insight live",
        "early_access": "Accesso anticipato",
        "unlock_now": "Sblocca ora",
        "top_teams_today": "Top squadre di oggi",
        "hot": "Hot",
        "cold": "Cold",
        "to_live_area": "Vai all'area live",
        "footer_text": "Pronostici calcistici con AI per i migliori campionati d'Europa.",
        "navigation": "Navigazione",
        "matches": "Matches",
        "predictions": "Predictions",
        "stats": "Stats",
        "legal": "Legale",
        "imprint": "Impressum",
        "privacy": "Privacy",
        "terms": "Termini",
        "stay_updated": "Stay Updated",
        "newsletter_text": "Ricevi i migliori pronostici via e-mail.",
        "email_placeholder": "La tua e-mail",
        "subscribe": "Abbonati",
        "points": "Punti",
        "draw": "Pareggio",
        "home_win": "Vittoria casa",
        "over_goals": "Oltre 2.5 gol",
        "under_goals": "Sotto 3.5 gol",
        "all_rights_reserved": "Tutti i diritti riservati."
    }
}


# =========================================================
# FORMATTER
# =========================================================
def format_kickoff_fd(utc_value: str) -> str:
    if not utc_value:
        return "-"
    try:
        dt = datetime.fromisoformat(utc_value.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return utc_value


def format_kickoff_api2(date_value: str) -> str:
    if not date_value:
        return "-"
    try:
        dt = datetime.fromisoformat(date_value.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return date_value


# =========================================================
# PREFERENCES
# =========================================================
def get_user_preferences():
    query_lang = request.args.get("lang")
    query_league = request.args.get("league")

    cookie_lang = request.cookies.get("preferred_lang")
    cookie_league = request.cookies.get("preferred_league")
    manual_override = request.cookies.get("manual_override", "false")

    if query_lang or query_league:
        final_lang = query_lang or cookie_lang or DEFAULT_PREFS["lang"]
        final_league = query_league or cookie_league or DEFAULT_PREFS["league"]

        if final_lang not in TRANSLATIONS:
            final_lang = DEFAULT_PREFS["lang"]

        if final_league not in LEAGUES:
            final_league = DEFAULT_PREFS["league"]

        return {
            "lang": final_lang,
            "league": final_league,
            "manual_override": True
        }

    if manual_override == "true" and cookie_lang and cookie_league:
        final_lang = cookie_lang if cookie_lang in TRANSLATIONS else DEFAULT_PREFS["lang"]
        final_league = cookie_league if cookie_league in LEAGUES else DEFAULT_PREFS["league"]

        return {
            "lang": final_lang,
            "league": final_league,
            "manual_override": True
        }

    auto_defaults = get_auto_defaults_from_country()
    return {
        "lang": auto_defaults["lang"],
        "league": auto_defaults["league"],
        "manual_override": False
    }


# =========================================================
# MATCH HELPERS
# =========================================================
def get_match_key(match: dict) -> str:
    return f"{match.get('home', '')}-{match.get('away', '')}"


def build_prediction_stub(matches):
    predictions = {}

    for i, match in enumerate(matches):
        match_id = get_match_key(match)

        if i % 2 == 0:
            predictions[match_id] = {
                "result_key": "home_win",
                "confidence_percent": 68,
                "confidence_score": "8.2/10",
                "tip_key": "over_goals"
            }
        else:
            predictions[match_id] = {
                "result_key": "draw",
                "confidence_percent": 29,
                "confidence_score": "6.7/10",
                "tip_key": "under_goals"
            }

    return predictions


# =========================================================
# PROVIDER
# =========================================================
def get_provider_for_league(league_key: str) -> str:
    return LEAGUE_PROVIDERS.get(league_key, "fd")


# =========================================================
# FOOTBALL-DATA
# =========================================================
def load_matches_fd(league_code: str):
    matches = []

    today = datetime.now(timezone.utc).date()
    future = today + timedelta(days=7)

    res = requests.get(
        f"{BASE_URL_FD}/competitions/{league_code}/matches?dateFrom={today}&dateTo={future}",
        headers=HEADERS_FD,
        timeout=20
    )
    res.raise_for_status()
    data = res.json()

    for m in data.get("matches", [])[:10]:
        home_team = m.get("homeTeam", {})
        away_team = m.get("awayTeam", {})
        score = m.get("score", {})
        full_time = score.get("fullTime", {})

        home_name = home_team.get("name", "Home")
        away_name = away_team.get("name", "Away")

        matches.append({
            "home": home_name,
            "away": away_name,
            "home_logo": find_logo(home_name),
            "away_logo": find_logo(away_name),
            "time": format_kickoff_fd(m.get("utcDate", "")),
            "status": m.get("status", ""),
            "score_home": full_time.get("home"),
            "score_away": full_time.get("away")
        })

    return matches


def load_table_fd(league_code: str):
    table = []

    res = requests.get(
        f"{BASE_URL_FD}/competitions/{league_code}/standings",
        headers=HEADERS_FD,
        timeout=20
    )
    res.raise_for_status()
    data = res.json()

    standings = data.get("standings", [])
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


def load_scorers_fd(league_code: str):
    scorers = []

    res = requests.get(
        f"{BASE_URL_FD}/competitions/{league_code}/scorers",
        headers=HEADERS_FD,
        timeout=20
    )
    res.raise_for_status()
    data = res.json()

    for s in data.get("scorers", [])[:10]:
        team = s.get("team", {})
        team_name = team.get("name", "")

        scorers.append({
            "name": s.get("player", {}).get("name", ""),
            "team": team_name,
            "logo": find_logo(team_name),
            "goals": s.get("goals", 0)
        })

    return scorers


# =========================================================
# API-FOOTBALL
# =========================================================
def load_matches_api2(league_id: int):
    matches = []

    today = datetime.now().strftime("%Y-%m-%d")
    future = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

    res = requests.get(
        f"{BASE_URL_API2}/fixtures",
        headers=HEADERS_API2,
        params={
            "league": league_id,
            "season": CURRENT_SEASON,
            "from": today,
            "to": future
        },
        timeout=20
    )
    res.raise_for_status()
    data = res.json()

    for m in data.get("response", [])[:10]:
        fixture = m.get("fixture", {})
        teams = m.get("teams", {})
        goals = m.get("goals", {})
        status = fixture.get("status", {})

        home = teams.get("home", {})
        away = teams.get("away", {})

        matches.append({
            "home": home.get("name", "Home"),
            "away": away.get("name", "Away"),
            "home_logo": home.get("logo", "/static/images/default.png"),
            "away_logo": away.get("logo", "/static/images/default.png"),
            "time": format_kickoff_api2(fixture.get("date", "")),
            "status": status.get("short", ""),
            "score_home": goals.get("home"),
            "score_away": goals.get("away")
        })

    return matches


def load_table_api2(league_id: int):
    table = []

    res = requests.get(
        f"{BASE_URL_API2}/standings",
        headers=HEADERS_API2,
        params={
            "league": league_id,
            "season": CURRENT_SEASON
        },
        timeout=20
    )
    res.raise_for_status()
    data = res.json()

    response = data.get("response", [])
    if not response:
        return table

    standings_groups = response[0].get("league", {}).get("standings", [])
    if not standings_groups:
        return table

    standings = standings_groups[0]

    for row in standings[:10]:
        team = row.get("team", {})
        table.append({
            "pos": row.get("rank", ""),
            "team": team.get("name", ""),
            "logo": team.get("logo", "/static/images/default.png"),
            "points": row.get("points", "")
        })

    return table


def load_scorers_api2(league_id: int):
    scorers = []

    res = requests.get(
        f"{BASE_URL_API2}/players/topscorers",
        headers=HEADERS_API2,
        params={
            "league": league_id,
            "season": CURRENT_SEASON
        },
        timeout=20
    )
    res.raise_for_status()
    data = res.json()

    for s in data.get("response", [])[:10]:
        player = s.get("player", {})
        statistics = s.get("statistics", [{}])[0]
        team = statistics.get("team", {})
        goals = statistics.get("goals", {})

        scorers.append({
            "name": player.get("name", ""),
            "team": team.get("name", ""),
            "logo": team.get("logo", "/static/images/default.png"),
            "goals": goals.get("total", 0) or 0
        })

    return scorers


# =========================================================
# WRAPPERS
# =========================================================
def load_matches(league_key: str):
    provider = get_provider_for_league(league_key)
    league_ref = LEAGUES.get(league_key)

    if not league_ref:
        return []

    if provider == "fd":
        return load_matches_fd(league_ref)

    return load_matches_api2(league_ref)


def load_table(league_key: str):
    provider = get_provider_for_league(league_key)
    league_ref = LEAGUES.get(league_key)

    if not league_ref:
        return []

    if provider == "fd":
        return load_table_fd(league_ref)

    return load_table_api2(league_ref)


def load_scorers(league_key: str):
    provider = get_provider_for_league(league_key)
    league_ref = LEAGUES.get(league_key)

    if not league_ref:
        return []

    if provider == "fd":
        return load_scorers_fd(league_ref)

    return load_scorers_api2(league_ref)


# =========================================================
# ROUTES
# =========================================================
@app.route("/")
def home():
    prefs = get_user_preferences()

    lang = prefs["lang"]
    league_key = prefs["league"]
    t = get_translation(lang)

    matches = []
    table = []
    scorers = []
    featured_match = None
    predictions = {}
    error = None

    try:
        provider = get_provider_for_league(league_key)

        if provider == "fd" and not API_KEY:
            raise Exception("API_KEY fehlt. Bitte in Render setzen.")

        if provider == "api2" and not API_FOOTBALL_KEY:
            raise Exception("API_FOOTBALL_KEY fehlt. Bitte in Render setzen.")

        matches = load_matches(league_key)
        table = load_table(league_key)
        scorers = load_scorers(league_key)

        if matches:
            live_statuses = {"IN_PLAY", "LIVE", "PAUSED"}
            live_matches = [
                m for m in matches
                if str(m.get("status", "")).upper() in live_statuses
            ]
            featured_match = live_matches[0] if live_matches else matches[0]

        predictions = build_prediction_stub(matches)

    except Exception as e:
        error = str(e)

    response = make_response(render_template(
        "index.html",
        matches=matches,
        table=table,
        scorers=scorers,
        featured_match=featured_match,
        predictions=predictions,
        get_match_key=get_match_key,
        error=error,
        league=league_key,
        lang=lang,
        t=t,
        is_premium=False
    ))

    max_age = 60 * 60 * 24 * 365
    response.set_cookie("preferred_lang", lang, max_age=max_age)
    response.set_cookie("preferred_league", league_key, max_age=max_age)

    if prefs["manual_override"]:
        response.set_cookie("manual_override", "true", max_age=max_age)

    return response


@app.route("/api/live-matches")
def api_live_matches():
    league_key = request.args.get("league", "bundesliga")

    try:
        provider = get_provider_for_league(league_key)

        if provider == "fd" and not API_KEY:
            return jsonify({"success": False, "error": "API_KEY fehlt", "matches": []})

        if provider == "api2" and not API_FOOTBALL_KEY:
            return jsonify({"success": False, "error": "API_FOOTBALL_KEY fehlt", "matches": []})

        matches = load_matches(league_key)
        return jsonify({"success": True, "matches": matches})

    except Exception as e:
        return jsonify({"success": False, "error": str(e), "matches": []})


if __name__ == "__main__":
    app.run(debug=True)