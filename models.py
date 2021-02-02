"""SQL Models for Reddit Stock Heatmap Project"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Subreddit(db.Model):
    """Subreddit model"""
    # subreddit names are letters only, no spaces. No checking is done here
    __tablename__ = "subreddits"

    id = db.Column(db.Integer, autoincrement = True, nullable = False, primary_key = True)
    name = db.Column(db.String(120), unique = True)
    weight = db.Column(db.Integer, nullable = False, default = 0)

    def __repr__(self):
        return f"<Subreddit: {self.name} id: {self.id} weight: {self.weight}>"

class Symbol(db.Model):
    """Symbol model for stock ticker symbols"""

    __tablename__ = "symbols"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    symbol = db.Column(db.String(20), unique = True)
    name = db.Column(db.String(300), nullable = False)
    default = db.Column(db.Boolean, nullable = False, default = False)
    index_id = db.Column(db.Integer, db.ForeignKey('indexes.id', ondelete = 'cascade'))
    index = db.relationship("Index")
    heat = db.relationship("RedditHeat", backref = "symbol")

    def __repr__(self):
        return f"<Symbol: {self.symbol}, name: {self.name}>"

class RedditHeat(db.Model):
    """RedditHeat model for a ticker symbol
    Heat is just the number of search results for the symbol per day.
    Also includes the stocks actual open/close price for the date (if any)"""

    __tablename__ = "reddit_heat"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    symbol_id = db.Column(db.Integer, db.ForeignKey('symbols.id', ondelete = 'cascade'))
    date = db.Column(db.DateTime, nullable = False)
    heat = db.Column(db.Integer, nullable = False, default = 0)
    open_price = db.Column(db.Float(precision = 2), nullable = True)
    close_price = db.Column(db.Float(precision = 2), nullable = True)
    percent_change = db.Column(db.Float(precision = 2), nullable = True)

    def __repr__(self):
        return f"<RedditHeat: {self.date.month}/{self.date.day}/{self.date.year} {self.symbol.symbol} {self.heat}>"

class Index(db.Model):
    """Index model for various stock market/indexes (S&P 500, DOW, etc...)"""

    __tablename__ = "indexes"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(300), nullable = False)
    symbol = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"<Index: {self.symbol}, {self.name}>"

class User(db.Model):
    """User model - stores user info as well as the auth and hash_pwd  classmethods"""
    
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    pw_hash = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(300), nullable = True) #* Not asking for at signup but leaving in the model
    symbols = db.relationship("Symbol", secondary = "users_symbols")

    def __repr__(self):
        return f"<User Obj: {self.username}"

    @classmethod
    def auth(cls, username, password):
        """
        Classmethod:
            Looks for the user with the given username and if user exists checks password provided to DB
        Usage:
            User.auth("username", "password")
            username and password are expcted to be strings
        Returns:
            If a user is found AND the password is correct returns the user object,
            False on username not found OR password incorrect
        Caution:
            No error checking of any sort is completed in this function
        """
        user = User.query.filter_by(username = username).first()
        bcrypt = Bcrypt()

        if user and bcrypt.check_password_hash(user.pw_hash, password):
            return user
        else:
            return False
    
    @classmethod
    def hash_pwd(cls, pwd):
        """
        Classmethod:
            Uses [flask] Bcrypt to hash a supplied password and return a string [utf-8] of that password
        Usage:
            User.hash_pwd("password as a string")
        Returns:
            utf-8 string of hashed password
        Caution:
            No error checking of any sort is completed here. It's assumed the error checking is made via other methods
            prior to calling this function, i.e. by WTForms
        """

        bcrypt = Bcrypt()
        temp_hashed = bcrypt.generate_password_hash(pwd)

        return temp_hashed.decode("utf8")

class UserSymbol(db.Model):
    """Models user's tracked symbols"""

    __tablename__ = "users_symbols"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'), primary_key = True)
    symbol_id = db.Column(db.Integer, db.ForeignKey('symbols.id', ondelete = 'cascade'), primary_key = True)


def connect_db(app):
    """Connects to the Database"""
    db.app = app
    db.init_app(app)