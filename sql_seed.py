from app import db
from models import Subreddit, Symbol, RedditHeat, Index, User, UserSymbol

db.drop_all()
db.create_all()