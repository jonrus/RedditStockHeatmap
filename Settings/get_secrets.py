# Used to get secrets when running local or via deployment.
# Heroku only gets what's push via gia and the secret file is ignored.
import os

# Check for the config var that tells us where to look
deployed_to_heroku = os.environ.get('DEPLOYED_ON_HEROKU', False)

if deployed_to_heroku:
    client_id = os.environ.get('REDDIT_CLIENT_ID')
    client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
    user_agent = os.environ.get('REDDIT_USER_AGENT')
    device_id = os.environ.get('REDDIT_DEVICE_ID')
    flask_secret_key = os.environ.get('SECRET_KEY')
else:
    import Settings.secret as secret # Import now, so we don't throw an error
    client_id = secret.client_id
    client_secret = secret.client_secret
    user_agent = secret.user_agent
    device_id = secret.device_id
    flask_secret_key = secret.flask_secret_key
