from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Blueprint, render_template
import os

from backend.routes.auth_routes import auth_bp
from backend.routes.crop_routes import crop_bp
from backend.routes.weather_routes import weather_bp
from backend.routes.soil_routes import soil_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.analyze import page_bp

load_dotenv()

app = Flask(__name__, template_folder="templets", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY")
CORS(app)

# ---------------- BLUEPRINTS ----------------
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(crop_bp, url_prefix="/crop") 
app.register_blueprint(weather_bp, url_prefix="/weather")
app.register_blueprint(soil_bp, url_prefix="/soil")
app.register_blueprint(dashboard_bp)
app.register_blueprint(page_bp)    
# app.register_blueprint(analyze_bp, url_prefix="/")



# ---------------- ROUTES FOR UI ----------------
@app.route("/")
def login_page():
    return render_template("login.html")   # frontend/login.html


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")  # frontend/dashboard.html

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

# ui_bp = Blueprint("ui_routes", __name__)

@app.route("/analyze")
def analyze_page():
    return render_template("analyze.html")




if __name__ == "__main__":
    app.run(debug=True)
