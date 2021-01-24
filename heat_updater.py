from RedditSearch import RedditSearch
import Helpers.helpers as helpers
import Settings.secret as secret
from app import db
from models import db, connect_db, Subreddit, Symbol, RedditHeat


reddit = RedditSearch(secret.client_id, secret.client_secret, secret.user_agent, secret.device_id)
if reddit.get_token():
    all_stocks = Symbol.query.all()
    all_subs = Subreddit.query.all()
    for stock in all_stocks:
        total_heat = 0
        for sub in all_subs:
            date_to_start = "2021-01-21 00:00:00+0000"
            date_to_find = "2021-01-22 00:00:00+0000"
            res = reddit.search_slice(term = stock.name, subreddit = sub.name, start_time = date_to_start, end_time = date_to_find)
            if res['res_data']['error']:
                print(res['res_data'])
            else:
                total_heat += res['res_data']['total_found']
                print(f"Sub: {sub.name} Symbol: {stock.symbol} Found: {res['res_data']['total_found']}")
        
        print(f"Symbol: {stock.symbol} Total Heat: {total_heat}")
        new_heat = RedditHeat(symbol_id = stock.id, date = date_to_find[:10], heat = total_heat) 
        db.session.add(new_heat)
        db.session.commit()
    