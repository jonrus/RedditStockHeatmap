# Reddit Stock Heatmap
This app, searches Reddit for the number of time a stock symbol is found, creating a value called 'Reddit Heat Index' for the current (as of 01/20/2021) S&P 500 Index stocks. The values are displayed on a daily (UTC based) heatmap, for stocks with at least one Reddit search hit. 
## Database Schema
- [Layout](Database%20Schema/db.png)
## API(s) Used
- [Reddit](https://www.reddit.com/dev/api/)
## Tools Used
- Javascript
  - [Axios](https://github.com/axios/axios)
  - [D3 Bubble Chart](https://observablehq.com/@d3/bubble-chart)
  - [Google Charts Line Chart](https://developers.google.com/chart/interactive/docs/gallery/linechart)
- CSS
  - [Bootstrap](https://getbootstrap.com/)
- HTML
- Python
  - [Flask](https://flask.palletsprojects.com/en/1.1.x/)
  - [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
  - [Flask-Jinja](https://flask.palletsprojects.com/en/1.1.x/templating/)
  - [Flask-WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
  - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Git](https://git-scm.com/)
- [GitHub](https://github.com/jonrus/RedditStockHeatmap)
- Deployment
  - [Heroku](https://www.heroku.com/)
## Screen Shots
- [Main Page](Screens/MainPage.png)
- [User Limited Stock Heatmap](Screens/CustomList.png)
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
- To update/fetch live data run heat_updater.py. It will search Reddit for the stock symbols in the four default tracked subreddits. The search should take about 20 minutes to finish. The script will update the database as it runs. As soon as any data is found, it is updated and viewable on the web front end.
