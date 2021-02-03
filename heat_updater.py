from RedditSearch import RedditSearch
import Helpers.helpers as helpers
import Settings.get_secrets as secret
from app import db
from models import db, connect_db, Subreddit, Symbol, RedditHeat
import time

def update_heat(date_to_find, date_to_start):
    """Dates are expected to look like;
    YYYY-MM-DD hh:mm:ss+Timezone
    i.e.
    2021-01-20 00:00:00+0000
    By default all searches are done at 00:00:00+0000 of whatever date."""
    reddit = RedditSearch(secret.client_id, secret.client_secret, secret.user_agent, secret.device_id)
    if reddit.get_token():
        all_stocks = Symbol.query.all()
        all_subs = Subreddit.query.all()
        for stock in all_stocks:
            total_heat = 0
            for sub in all_subs:
                res = reddit.search_slice(
                    term = stock.name,
                    subreddit = sub.name,
                    start_time = date_to_start,
                    end_time = date_to_find
                    )
                if res['res_data']['error']:
                    #TODO: Do something here...
                    pass
                else:
                    total_heat += res['res_data']['total_found']
                    print(f"Sub: {sub.name} Symbol: {stock.symbol} Found: {res['res_data']['total_found']}")
            
            print(f"Symbol: {stock.symbol} Total Heat: {total_heat}")
            new_heat = RedditHeat(symbol_id = stock.id, date = date_to_find[:10], heat = total_heat) 
            db.session.add(new_heat)
            db.session.commit()
    
if __name__ == "__main__":
    now = round(time.time()) + 0.0
    start_date = time.strftime("%Y-%m-%d 00:00:00+0000", time.gmtime(now))
    find_date = time.strftime("%Y-%m-%d 00:00:00+0000", time.gmtime(now - 86400.0)) #* Subtract 1 day.

    update_heat(find_date, start_date)