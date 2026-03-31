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

TRANSLATIONS = {
    "de": {
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
        "top_matches_sub": "Heute wichtigste Spiele & Vorhersagen",
        "prediction": "Prediction",
        "confidence": "Confidence",
        "details": "Details",
        "tip": "Tipp",
        "tip_premium_only": "Nur für Premium",
        "unlock_premium": "Premium freischalten",
        "prediction_premium_only": "Prediction nur für Premium",
        "prediction_locked_text": "Vorhersagen, Confidence und Tipps werden nach Abo-Freischaltung angezeigt.",
        "live_in_play": "Live & In-Play",
        "live_in_play_sub": "Echtzeit Vorhersagen & Updates",
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
        "subscribe": "Abonnieren"
    },
    "en": {
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
        "live_in_play": "Live & In-Play",
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
        "subscribe": "Subscribe"
    },
    "fr": {
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
        "live_in_play": "Live & In-Play",
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
        "subscribe": "S'abonner"
    },
    "it": {
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
        "live_in_play": "Live & In-Play",
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
        "subscribe": "Abbonati"
    }
}


def get_translation():
    lang = request.args.get("lang", "de")
    if lang not in TRANSLATIONS:
        lang = "de"
    return lang, TRANSLATIONS[lang]


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

        matches.append({
            "home": home_team.get("name", "Home"),
            "away": away_team.get("name", "Away"),
            "home_logo": find_logo(home_team.get("name", "")),
            "away_logo": find_logo(away_team.get("name", "")),
            "time": format_kickoff(m.get("utcDate", "")),
            "status": m.get("status", ""),
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
    lang, t = get_translation()
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
        league=league_key,
        lang=lang,
        t=t,
        is_premium=False
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