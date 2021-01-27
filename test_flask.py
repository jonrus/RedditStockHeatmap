from unittest import TestCase

from app import app
from models import db, Subreddit, Symbol, RedditHeat, Index, User, UserSymbol

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reddit_heatmap_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()