from unittest import TestCase

from app import app
from models import db, Subreddit, Symbol, RedditHeat, Index, User, UserSymbol

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reddit_heatmap_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class SubredditTestCase(TestCase):
    """Subreddit is a simple model, not much to test"""
    def setUp(self):
        Subreddit.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_default_sub_weight(self):
        test_sub = Subreddit(name = "testSub")
        db.session.add(test_sub)
        db.session.commit()
        self.assertEqual(test_sub.weight, 0)

class SymbolTestCase(TestCase):
    """Symbol model test case"""
    def setUp(self):
        Symbol.query.delete()
        Index.query.delete()
        RedditHeat.query.delete()

    def tearDown(self):
        db.session.rollback()

    