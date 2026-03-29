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
        "register": "Registrieren",
        "premium": "Premium",
        "forgot_title": "Passwort zurücksetzen",
        "forgot_text": "Gib deine E-Mail-Adresse ein. Später senden wir dir einen Link zum Zurücksetzen deines Passworts.",
        "forgot_button": "Reset-Link senden",
        "back_to_login": "Zurück zum Login",
        "nav": {
            "bundesliga": "Deutschland",
            "premierleague": "England",
            "seriea": "Italien",
            "ligue1": "Frankreich",
            "championsleague": "Champions League",
            "euro": "EURO",
            "worldcup": "WM",
            
        },
        "hero_title": "Fussball Statistiken mit Vertrauen",
        "hero_text": "Live Spiele, kommende Partien, Tabellen und Top Scorer. Premium Analysen, Prognosen und Wahrscheinlichkeiten nach Login.",
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
        "premium_box_text": "Mit Gewinnwahrscheinlichkeiten, Head-to-Head, Formanalyse und weiteren Premium Features.",
        "premium_button": "Mehr erfahren",
        "login_title": "Willkommen zurück",
        "login_text": "Melde dich an, um Premium Prognosen, gespeicherte Favoriten und tiefere Analysen zu sehen.",
        "email": "E-Mail",
        "password": "Passwort",
        "forgot_password": "Passwort vergessen?",
        "login_button": "Jetzt einloggen",
        "register_title": "Konto erstellen",
        "register_text": "Erstelle dein Konto, um Premium Bereiche, personalisierte Statistiken und spätere Prognosen zu nutzen.",
        "name": "Name",
        "confirm_password": "Passwort bestätigen",
        "register_button": "Konto erstellen",
        "premium_title": "Premium Analyse Bereich",
        "premium_text": "Hier werden später exklusive Wahrscheinlichkeiten, Teamvergleiche, Formanalysen und Premium Dashboards freigeschaltet.",
        "premium_feature_1": "Gewinnwahrscheinlichkeiten",
        "premium_feature_2": "Head-to-Head Analysen",
        "premium_feature_3": "Form und Trend Modelle",
        "premium_feature_4": "Top Value Match Hinweise",
        "premium_feature_5": "Persönliche Favoriten",
        "premium_feature_6": "Werbefreier Bereich",
        "cta_register": "Jetzt registrieren",
        "cta_login": "Zum Login"
    },
    "en": {
        "brand": "MatchPredictions",
        "login": "Login",
        "register": "Register",
        "premium": "Premium",
        "forgot_title": "Reset password",
        "forgot_text": "Enter your email address. Later we will send you a password reset link.",
        "forgot_button": "Send reset link",
        "back_to_login": "Back to login",
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
        "hero_text": "Live matches, upcoming fixtures, standings and top scorers. Premium analysis, predictions and probabilities after login.",
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
        "premium_box_text": "With win probabilities, head-to-head, form analysis and more premium features.",
        "premium_button": "Learn more",
        "login_title": "Welcome back",
        "login_text": "Sign in to access premium predictions, saved favorites and deeper analysis.",
        "email": "Email",
        "password": "Password",
        "forgot_password": "Forgot password?",
        "login_button": "Login now",
        "register_title": "Create account",
        "register_text": "Create your account to unlock premium areas, personalized statistics and future predictions.",
        "name": "Name",
        "confirm_password": "Confirm password",
        "register_button": "Create account",
        "premium_title": "Premium analysis area",
        "premium_text": "Exclusive probabilities, team comparisons, form analysis and premium dashboards will be unlocked here later.",
        "premium_feature_1": "Win probabilities",
        "premium_feature_2": "Head-to-head analysis",
        "premium_feature_3": "Form and trend models",
        "premium_feature_4": "Top value match hints",
        "premium_feature_5": "Personal favorites",
        "premium_feature_6": "Ad free area",
        "cta_register": "Register now",
        "cta_login": "Go to login"
    },
    "it": {
        "brand": "MatchPredictions",
        "login": "Login",
        "register": "Registrati",
        "premium": "Premium",
        "forgot_title": "Reimposta password",
        "forgot_text": "Inserisci il tuo indirizzo e-mail. In seguito ti invieremo un link per reimpostare la password.",
        "forgot_button": "Invia link di reset",
        "back_to_login": "Torna al login",
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
        "hero_text": "Partite live, incontri in arrivo, classifiche e migliori marcatori. Analisi premium, pronostici e probabilità dopo il login.",
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
        "premium_box_text": "Con probabilità di vittoria, testa a testa, analisi della forma e altre funzioni premium.",
        "premium_button": "Scopri di più",
        "login_title": "Bentornato",
        "login_text": "Accedi per vedere pronostici premium, preferiti salvati e analisi più profonde.",
        "email": "E-mail",
        "password": "Password",
        "forgot_password": "Password dimenticata?",
        "login_button": "Accedi ora",
        "register_title": "Crea account",
        "register_text": "Crea il tuo account per sbloccare aree premium, statistiche personalizzate e futuri pronostici.",
        "name": "Nome",
        "confirm_password": "Conferma password",
        "register_button": "Crea account",
        "premium_title": "Area analisi premium",
        "premium_text": "Qui verranno sbloccate probabilità esclusive, confronti tra squadre, analisi della forma e dashboard premium.",
        "premium_feature_1": "Probabilità di vittoria",
        "premium_feature_2": "Analisi testa a testa",
        "premium_feature_3": "Modelli di forma e trend",
        "premium_feature_4": "Segnali top value match",
        "premium_feature_5": "Preferiti personali",
        "premium_feature_6": "Area senza pubblicità",
        "cta_register": "Registrati ora",
        "cta_login": "Vai al login"
    },
    "fr": {
        "brand": "MatchPredictions",
        "login": "Connexion",
        "register": "Inscription",
        "premium": "Premium",
        "forgot_title": "Réinitialiser le mot de passe",
        "forgot_text": "Saisis ton adresse e-mail. Plus tard nous t’enverrons un lien pour réinitialiser ton mot de passe.",
        "forgot_button": "Envoyer le lien de réinitialisation",
        "back_to_login": "Retour au login",
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
        "hero_text": "Matchs en direct, rencontres à venir, classements et meilleurs buteurs. Analyses premium, pronostics et probabilités après connexion.",
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
        "premium_box_text": "Avec probabilités de victoire, head-to-head, analyse de forme et autres fonctions premium.",
        "premium_button": "En savoir plus",
        "login_title": "Bon retour",
        "login_text": "Connecte-toi pour voir les pronostics premium, les favoris enregistrés et des analyses plus poussées.",
        "email": "E-mail",
        "password": "Mot de passe",
        "forgot_password": "Mot de passe oublié ?",
        "login_button": "Se connecter",
        "register_title": "Créer un compte",
        "register_text": "Crée ton compte pour débloquer les zones premium, les statistiques personnalisées et les futurs pronostics.",
        "name": "Nom",
        "confirm_password": "Confirmer le mot de passe",
        "register_button": "Créer un compte",
        "premium_title": "Zone analyse premium",
        "premium_text": "Ici seront débloqués plus tard des probabilités exclusives, comparaisons d équipes, analyses de forme et dashboards premium.",
        "premium_feature_1": "Probabilités de victoire",
        "premium_feature_2": "Analyses head-to-head",
        "premium_feature_3": "Modèles de forme et tendance",
        "premium_feature_4": "Indications top value match",
        "premium_feature_5": "Favoris personnels",
        "premium_feature_6": "Zone sans publicité",
        "cta_register": "S inscrire maintenant",
        "cta_login": "Aller au login"
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
                table.append({
                    "pos": row.get("position", ""),
                    "team": team.get("name", ""),
                    "short": team.get("shortName") or team.get("tla") or team.get("name", ""),
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

@app.route("/forgot-password")
def forgot_password():
    lang, t = get_translation()
    league = request.args.get("league", "bundesliga")
    return render_template("forgot_password.html", t=t, lang=lang, league=league)


if __name__ == "__main__":
    app.run(debug=True)