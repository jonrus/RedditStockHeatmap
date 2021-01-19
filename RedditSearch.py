import requests
import requests.auth
import json
import secret

class RedditSearch():
    """This class wrapper only performs searches via the reddit api.
    No other API features are included"""

    def __init__(self):
        self.__URL = "https://oauth.reddit.com"
        self.headers = {
            "User-Agent" : secret.user_agent
        }
        self.token = None

    def get_token(self, id, secret, device):
        """Uses the 'Application Only OAuth' method to get a token from reddit.
        """
        # TODO: Add error check and clean up
        
        auth_client = requests.auth.HTTPBasicAuth(id, secret)
        post_data = {
            "grant_type" : "https://oauth.reddit.com/grants/installed_client",
            "device_id" : device
        }

        res = requests.post("https://www.reddit.com/api/v1/access_token", headers = self.headers, auth = auth_client, data = post_data)
        j = res.json()
        token = j["access_token"]
        token_type = j["token_type"]

        # Add auth to header
        self.headers["Authorization"] = f"{token_type} {token}"
        print(f"Headers: {self.headers}")

    def search(self, term, after = None):
        # TODO: Add error checking
        # TODO: Add rate limit checking
        # TODO: Add pagination support
        if after == None:
            params = {
                "q" : term
                # "limit" : 2
            }
        else:
            params = {
                "q" : term,
                "after" : after
            }

        res = requests.get(f"{self.__URL}/search.json", params = params, headers = self.headers)
        print(res.url)
        print(res.headers)
        # j = res.json()
        # print(j["kind"])
        # print(res.text)
        return res.json()

if __name__ == "__main__":
    reddit = RedditSearch()
    reddit.get_token(secret.client_id, secret.client_secret, secret.device_id)
    results = reddit.search("tsla")
    for item in results["data"]["children"]:
        print(f"Name: {item['data']['name']}")