from flask import Flask
from app.routes.home import home_bp
from app.routes.matches import matches_bp

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(matches_bp)