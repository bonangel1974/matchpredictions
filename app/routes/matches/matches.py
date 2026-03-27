from flask import Blueprint, render_template

matches_bp = Blueprint("matches", __name__)

@matches_bp.route("/matches")
def matches():
    sample_matches = [
        {
            "league": "Premier League",
            "home_team": "Arsenal",
            "away_team": "Chelsea",
            "date": "27.03.2026",
            "time": "20:30"
        },
        {
            "league": "Bundesliga",
            "home_team": "Bayern München",
            "away_team": "Borussia Dortmund",
            "date": "28.03.2026",
            "time": "18:30"
        },
        {
            "league": "Serie A",
            "home_team": "Inter",
            "away_team": "Juventus",
            "date": "29.03.2026",
            "time": "20:45"
        }
    ]

    return render_template("matches.html", matches=sample_matches)