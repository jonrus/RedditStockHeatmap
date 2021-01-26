import os
from datetime import date
from flask import Flask, render_template, jsonify, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Subreddit, Symbol, RedditHeat, Index, User, UserSymbol
import Settings.secret as secret

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///reddit_heatmap'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secret.flask_secret_key)
toolbar = DebugToolbarExtension(app)

connect_db(app)

#***********************************
#* Helper Functions
#***********************************
def get_reddit_heat_by_date(date, cutoff = 1):
    heat_data = []
    all_heat = RedditHeat.query.filter_by(date=date).all()
    for stock in all_heat:
        if stock.heat >= cutoff:
            heat_data.append(
                {
                    "Name" : stock.symbol.name,
                    "Count" : stock.heat,
                    "Symbol" : stock.symbol.symbol
                }
            )
    return heat_data

#***********************************
#* Webview Routes
#***********************************
@app.route("/")
def root_route():
    return render_template("root.html")
    


#***********************************
#* API Style Routes
#***********************************
@app.route("/api/latest", methods = ["GET"])
def api_latest_route():
    """Returns the newest (by date) complete set of Reddit Heat data as JSON"""
    return jsonify(get_reddit_heat_by_date("2021-01-21"))


#***********************************
#* Testing Routes
#***********************************
@app.route("/render_all")
def render_all_route():
    import pdb; pdb.set_trace()
