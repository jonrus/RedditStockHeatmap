# Reddit Stock Heatmap

## Database Schema
- [Layout](Database%20Schema/db.png)

## APIs Used
- [Reddit](https://www.reddit.com/dev/api/) 
- [IEX Cloud](https://iexcloud.io/) 
- [Alpha Vantage](https://www.alphavantage.co/) 
- Market API TBD based on usage and rate limits/needs

## Requirements
- See requirements.txt for required Python modules
  - Use pip install -r requirements.txt - for a quick install of all modules
- [PostgresSQL](https://www.postgresql.org/) installed and configured on system
- Configure example_secret.py (in Settings Dir) as required
  - Rename example_secret.py to secret.py