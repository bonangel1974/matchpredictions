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
        }
    ]

    return render_template("matches.html", matches=sample_matches)