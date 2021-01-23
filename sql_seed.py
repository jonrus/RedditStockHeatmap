from app import db
from models import Subreddit, Symbol, RedditHeat, Index, User, UserSymbol

db.drop_all()
db.create_all()
# Create seed subs
sub1 = Subreddit(name = "investing")
sub2 = Subreddit(name = "stocks")
db.session.add_all([sub1, sub2])
db.session.commit()

# Create seed Indexes
nyse = Index(name = "New York Stock Exchange", symbol = "NYSE")
nasdaq = Index(name = "Nasdaq", symbol = "NASDAQ")
db.session.add_all([nyse, nasdaq])
db.session.commit()

# Create some seed Stock Symbols
tsla = Symbol(symbol = "TSLA", name = "Tesla, Inc", index_id = nasdaq.id)
appl = Symbol(symbol = "APPL", name = "Apple, Inc", index_id = nasdaq.id)
amzn = Symbol(symbol = "AMZN", name = "Amazon.com, Inc", index_id = nasdaq.id)
ge = Symbol(symbol = "GE", name = "General Electric Company", index_id = nyse.id)
dis = Symbol(symbol = "DIS", name = "Walt Disney Co.", index_id = nyse.id)
dal = Symbol(symbol = "DAL", name = "Delta Air Lines, Inc.", index_id = nyse.id)
db.session.add_all([tsla, appl, amzn, ge, dis, dal])
db.session.commit()