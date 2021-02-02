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

class UserTestCase(TestCase):
    """Tests User model and it's class methods"""
    def setUp(self):
        User.query.delete()

    def tearDown(self):
        db.session.rollback()

    def test_new_user(self):
        # For this test, use an unhashed password, by setting it directly
        new_user = User(username = "TEST_USER", pw_hash = "password")

        db.session.add(new_user)
        db.session.commit()

        self.assertIsNotNone(new_user.id)
    
    def test_pw_correct_pw(self):
        # Test the pw_hash and auth classmethods with a correct password
        hashed_pw = User.hash_pwd("password")
        new_user = User(username = "New_User", pw_hash = hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        login_user = User.auth(new_user.username, "password")

        self.assertIsInstance(login_user, User)


    def test_pw_incorrect_pw(self):
        # Test the pw_hash and auth classmethods with an incorrect Password
        hashed_pw = User.hash_pwd("password")
        new_user = User(username = "New_User", pw_hash = hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        login_user = User.auth(new_user.username, "Password")

        self.assertIs(login_user, False)

    def test_pw_incorrect_uname(self):
        # Test the pw_hash and auth classmethods with an incorrect Password
        hashed_pw = User.hash_pwd("password")
        new_user = User(username = "Correct_UserName", pw_hash = hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        login_user = User.auth("Incorrect_Username", "password")

        self.assertIs(login_user, False)