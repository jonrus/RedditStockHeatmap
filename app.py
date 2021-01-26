import os
from datetime import date
from flask import Flask, render_template, jsonify, request#, flash, redirect, session # Uncomment as start to use
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
    newest = RedditHeat.query.order_by(RedditHeat.date.desc()).first()
    oldest = RedditHeat.query.order_by(RedditHeat.date).first()
    return render_template("bubble_map.html", newest_data_date = str(newest.date)[:10], oldest_data_date = str(oldest.date)[:10])
    
@app.route("/sym/<sym>")
def view_symbol_route(sym):
    return render_template("line_chart.html", symbol = sym)

@app.route("/about")
def about_route():
    # TODO: This route
    return "to do"

@app.route("/signup")
def signup_route():
    # TODO: This route
    return "to do"

@app.route("/login")
def login_route():
    # TODO: This route
    return "to do"

#***********************************
#* API Style Routes
#***********************************
@app.route("/api/latest", methods = ["GET"])
def api_latest_route():
    """Returns the newest (by date) complete set of Reddit Heat data as JSON"""
    newest = RedditHeat.query.order_by(RedditHeat.date.desc()).first()
    return jsonify(get_reddit_heat_by_date(str(newest.date)[:10]))

@app.route("/api/date/<date>", methods = ["GET"])
def api_bydate_route(date):
    """Returns the data for the given date"""
    heat_limit = int(request.args.get('heat', 1))
    return jsonify(get_reddit_heat_by_date(date=date, cutoff= heat_limit))

@app.route("/api/sym/<sym>", methods = ["GET"])
def api_symbol_data(sym):
    found_sym = Symbol.query.filter_by(symbol=sym).first()
    if found_sym == None:
        res_data = {"error" : f"ERROR!! Unable to find any data for symbol - {sym}!"}
    else:
        res_data = {
            "chart" : {
                "title" : f"{found_sym.name}({found_sym.symbol}) - Reddit Heat over time"
            },
            "data" : []
        }
        for item in found_sym.heat:
            res_data['data'].append([str(item.date)[:10], item.heat])
    return jsonify(res_data)