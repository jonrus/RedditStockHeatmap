"""SQL Models for Reddit Stock Heatmap Project"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Subreddit(db.Model):
    """Subreddit model"""

    __tablename__ = "subreddits"

    id = db.Column(db.Integer, autoincrement = True, nullable = False)
    name = db.Column(db.String(120), primary_key = True)
    weight = db.Column(db.Integer, nullable = False, default = 0)

class Symbol(db.Model):
    """Symbol model for stock ticker symbols"""

    __tablename__ = "symbols"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    symbol = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(300), nullable = False)
    index_id = db.Column(db.Integer, db.ForeignKey('indexes.id', ondelete = 'cascade'))
    index = db.relationship("Index")
    heat = db.relationship("RedditHeat")

class RedditHeat(db.Model):
    """RedditHeat model for a ticker symbol"""

    __tablename__ = "reddit_heat"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    symbol_id = db.Column(db.Integer, db.ForeignKey('symbols.id', ondelete = 'cascade'))
    date = db.Column(db.DateTime, nullable = False)
    heat = db.Column(db.Integer, nullable = False, default = 0)

class Index(db.Model):
    """Index model for various stock market/indexes (S&P 500, DOW, etc...)"""

    __tablename__ = "indexes"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(300), nullable = False)
    symbol = db.Column(db.String(20), nullable = False)

class User(db.Model):
    """User model - stores user info as well as helper methods to hash and auth a user"""
    
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    pw_hash = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(300), nullable = True)
    symbols = db.relationship("Symbol", secondary = "users_symbols")
    #TODO: Add Methods

class UserSymbol(db.Model):
    """Models user's tracked symbols"""

    __tablename__ = "users_symbols"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'), primary_key = True)
    symbol_id = db.Column(db.Integer, db.ForeignKey('symbols.id', ondelete = 'cascade'))


def connect_db(app):
    """Connects to the Database"""
    db.app = app
    db.init_app(app)