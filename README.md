# Reddit Stock Heatmap
This app, searches Reddit for a number of time a stock symbol is found, creating a value called 'Reddit Heat Index' for the current (as of 01/20/2021) S&P 500 Index stocks. The values are displayed on a daily (UTC based) heatmap, for stocks with at least one Reddit search hit. 
## Database Schema
- [Layout](Database%20Schema/db.png)
## API(s) Used
- [Reddit](https://www.reddit.com/dev/api/) 
## Requirements
- See requirements.txt for required Python modules
  - Use pip install -r requirements.txt - for a quick install of all modules
- [PostgresSQL](https://www.postgresql.org/) installed and configured on system
  - Create a database called 'reddit_heat' OR update app.py with the database name you've used.
  - Create a database called 'reddit_heat_test' if you want to run the tests OR update test_sql_models.py with the database name you've used.
- Obtain [Reddit API](https://www.reddit.com/wiki/api) access.
- Configure example_secret.py (in Settings Dir) as required
  - Rename example_secret.py to secret.py
## Setup/Running
- To view sample seed data run the file sql_seed.py and start the flask app (flask run) you will have a working app with seed data. 