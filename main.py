from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():

    lang = request.args.get("lang", "de")

    translations = {
        "de": {
            "brand": "Football Stats",
            "nav1": "Bundesliga Stats",
            "nav2": "Champions League Stats",
            "nav3": "Premier League Stats",
            "nav4": "EM 2024 Stats",
            "login": "Login",
            "hero_status": "Bundesliga Live Status",
            "possession": "Ballbesitz",
            "shots": "Schüsse gesamt",
            "xg": "xG",
            "team_stats": "Team Statistiken",
            "top_teams": "Top Teams",
            "search_placeholder": "Suche Teams, Spieler oder Statistiken ...",
            "player_stats": "Spieler Statistiken",
            "top_scorer": "Top Scorer",
            "top_assists": "Top Assists",
            "view_full_table": "Gesamte Tabelle ansehen",
            "see_all_teams": "Alle Teams ansehen",
            "view_full_scorers": "Alle Torschützen ansehen",
            "view_all_assists": "Alle Assist-Leader ansehen",
            "trust_title": "Kostenlose Statistiken & Live-Daten",
            "trust_text": "Öffentliche Statistiken schaffen Vertrauen.",
            "premium_title": "Mehr Analysen nach Login",
            "premium_text": "Premium Features nach Registrierung.",
            "learn_more": "Mehr erfahren",
            "register_now": "Login / Registrieren",
        },
        "en": {
            "brand": "Football Stats",
            "nav1": "Bundesliga Stats",
            "nav2": "Champions League Stats",
            "nav3": "Premier League Stats",
            "nav4": "Euro 2024 Stats",
            "login": "Login",
            "hero_status": "Bundesliga Live Status",
            "possession": "Ball Possession",
            "shots": "Total Shots",
            "xg": "xG",
            "team_stats": "Team Statistics",
            "top_teams": "Top Teams",
            "search_placeholder": "Search teams...",
            "player_stats": "Player Statistics",
            "top_scorer": "Top Scorers",
            "top_assists": "Top Assists",
            "view_full_table": "View Full Table",
            "see_all_teams": "See All Teams",
            "view_full_scorers": "View Full Scorers",
            "view_all_assists": "View All Assist Leaders",
            "trust_title": "Free stats & live data",
            "trust_text": "Public stats build trust.",
            "premium_title": "More analysis after login",
            "premium_text": "Premium features unlocked.",
            "learn_more": "Learn more",
            "register_now": "Login / Register",
        }
    }

    t = translations.get(lang, translations["de"])

    return render_template(
        "index.html",
        t=t,
        lang=lang,
        table_rows=[
            ["Bayern Munich", "30", "+39", "65"],
            ["Borussia Dortmund", "30", "+8", "65"],
        ],
        scorers=[
            ["H. Kane", "Bayern", "28", "28"]
        ],
        assists=[
            ["K. De Bruyne", "City", "16", "18"]
        ],
        top_teams_left=["Arsenal", "Inter"],
        top_teams_right=["Juventus", "Milan"]
    )


if __name__ == "__main__":
    app.run(debug=True)