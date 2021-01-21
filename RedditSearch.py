import requests
import requests.auth
import secret
import helpers

class RedditSearch():
    """This Reddit API wrapper, is bare bones and provides autherzation and search features only."""

    def __init__(self, client_id, client_secret, user_agent, device_id):
        self.__URL = "https://oauth.reddit.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.device_id = device_id
        self.headers = {
            "User-Agent" : self.user_agent
        }
        self.token = None
        self.authorized = False

    def get_token(self):
        """Uses the 'Application Only OAuth' method to get a token from reddit.
        """
        auth_client = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        post_data = {
            "grant_type" : "https://oauth.reddit.com/grants/installed_client",
            "device_id" : self.device_id
        }

        res = requests.post("https://www.reddit.com/api/v1/access_token", headers = self.headers, auth = auth_client, data = post_data)
        if res.status_code != requests.codes.ok:
            print(f"Unable to get token - status code: {res.status_code}") #*DELETE
            return False

        # Extract token and access type from returned JSON
        j = res.json() #TODO Add Error Catch
        token = j["access_token"]
        token_type = j["token_type"]

        # Add auth to header
        self.headers["Authorization"] = f"{token_type} {token}"
        self.authorized = True

        return True

    def search(self, term, subreddit = "all", limit = 25, limit_to_sub = False, sort = "new", nsfw = True, before = None, after = None, verbose = False):
        """Perform a basic search or slice of the given subreddit for the given term.
        limit can be between 0 and 100
        sort defaults to new can be one of ['relevance', 'hot', 'top', 'new', 'comments']
        verbose set to true will provide additonal console output.
        after/before must be set to a thing name - results are non inclusive"""
        # TODO: Use sessions???
        # TODO: Add more error checking
        # TODO: Add rate limit checking
        
        # Simple error check to limit 'limit' to okay values
        if limit > 100 or limit < 0:
            limit = 25

        # Check is sort is an okay value
        if sort not in ['relevance', 'hot', 'top', 'new', 'comments']:
            return False #TODO Return a dict - will cause error on search_until
        
        # Construct search params
        params = {
            "q" : term,
            "sort" : sort,
            "limit" : limit,
            "include_over_18" : nsfw,
            "restrict_sr" : limit_to_sub,
            "before" : before,
            "after" : after
        }
        res = requests.get(f"{self.__URL}/r/{subreddit}/search.json", params = params, headers = self.headers)
        
        # Simple check and return false if the request was unable to complete
        if res.status_code != requests.codes.ok:
            return False #TODO Return a dict - will cause error on search_until

        # Convert results to JSON
        j = res.json() #TODO Add Error Catch

        # Add our search info to the JSON object
        j['search_data'] = {
            "subreddit" : subreddit,
            "term" : term,
            "sort" : sort,
            "limit" : limit,
            "limit_to_sub" : limit_to_sub,
            "before" : before,
            "after" : after
        }

        # Add our custom result data to the JSON object
        res_count = len(j['data']['children'])
        if res_count < 1:
            # No Results, return a different 'res_data'
            j['res_data'] = {
                "count" : 0, #* Hard code this to zero just to make things easier where it's being called
                "headers" : res.headers,
                "url" : res.url,
                "status_code" : res.status_code,
                "rate_limit_used" : res.headers.get("X-Ratelimit-Used", None),
                "rate_limit_remain" : res.headers.get("X-Ratelimit-Remaining", None),
                "rate_limit_reset" : res.headers.get("X-Ratelimit-Reset", None),
                "first_thing" : None,
                "first_thing_created_utc" : None,
                "last_thing" : None,
                "last_thing_created_utc" : None,
                "error" : "No results" #! No Results
            }
            return j

        j['res_data'] = {
            "count" : res_count,
            "headers" : res.headers,
            "url" : res.url,
            "status_code" : res.status_code,
            "rate_limit_used" : res.headers.get("X-Ratelimit-Used", None),
            "rate_limit_remain" : res.headers.get("X-Ratelimit-Remaining", None),
            "rate_limit_reset" : res.headers.get("X-Ratelimit-Reset", None),
            "first_thing" : j['data']['children'][0]['data']['name'],
            "first_thing_created_utc" : j['data']['children'][0]['data']['created_utc'],
            "last_thing" : j['data']['children'][res_count - 1]['data']['name'],
            "last_thing_created_utc" : j['data']['children'][res_count - 1]['data']['created_utc']
        }

        # Debug Printing
        if verbose:
            print(f"Generated URL: {j['res_data']['url']}")
            print(f"Rate Limit Used: {j['res_data']['rate_limit_used']}")
            print(f"Rate Limit Remain: {j['res_data']['rate_limit_remain']}")
            print(f"Rate Limit Reset: {j['res_data']['rate_limit_reset']}")
            # print(f"Response Headers: {j['res_data']['headers']}")
            print(f"First Thing: {j['res_data']['first_thing']}")
            print(f"Last Thing: {j['res_data']['last_thing']}")
            # print(f"Response Text: {res.text}")
            print(f"Results: {j['res_data']['count']}")

        return j


    def search_until(self, term, subreddit, until, max_searches = 100, limit_to_sub = True, verbose = False):
        """
        Important note: Due to reddit limitations this function will often fail when searching for more than five days.
            It really depends on the subreddit and how much activity there is.
            I've had good results with no more than five days on r/all, thus I would think less active subs would
            work further back in time.
            It provides very little error checking so use at your own risk...
        Performs a normal search, until it finds a thing at or after the given datetime.
        It then returns that thing name.
        until is expected to a string with date and time;
        example; '2021-01-01 12:00:00+0000'
        
        Expected Output;
        {
            "res_data" : {
                "thing" : "thingName", #* Name of thing or None if not found
                "thing_time" : epoch Time of Thing, #* Epoch time of thing or None if not found
                "total_found" : X, #* Sum total of all things that matched the search - valid even if max searches reached
                "error" : "error string" #* Human readable error string or None if no error
            },
            "thing_data" : {
                # All Returned reddit data or None if not found
            }
        }
        """

        # Do some setup...
        until = helpers.str_to_epoch(until) # Convert datetime string to epoch time
        found = False

        # Perform the first search
        search_res = self.search(term, subreddit, 100, True, verbose = verbose)
        if search_res['res_data']['count'] == 0:
            return {
                "res_data" : {
                    "thing" : None,
                    "thing_time" : None,
                    "total_found" : 0,
                    "error" : f"No results for '{term}' on r/{subreddit}"
                },
                "thing_data" : None
            }

        #Found at least 1 results work with it
        num_searches = 1
        total_found = 0
        while not found:
            total_found += search_res['res_data']['count']

            #* Do some error checking
            if num_searches > max_searches:
                return {
                    "res_data" : {
                        "thing" : None,
                        "thing_time" : None,
                        "total_found" : total_found,
                        "error" : "Reached max number of searches"
                    },
                    "thing_data" : None
                }
            if search_res['res_data']['count'] == 0:
                return {
                    "res_data" : {
                        "thing" : None,
                        "thing_time" : None,
                        "total_found" : total_found,
                        "error" : "Unable to find results as old as requested"
                    },
                    "thing_data" : None
                }
            
            # Check if we found a thing older than we're looking for
            if search_res['res_data']['last_thing_created_utc'] <= until:
                found = True
            else:
                # Nothing found yet, do a new 'after' search
                after_thing = search_res['res_data']['last_thing']
                search_res = self.search(term, subreddit, 100, True, after = after_thing, verbose = verbose)
                num_searches += 1

        # Loop to find the thing name that best matches our timeframe
        for item in search_res['data']['children']:
            if item['data']['created_utc'] <= until:
                return {
                    "res_data" : {
                        "thing" : item['data']['name'],
                        "thing_time" : item['data']['created_utc'],
                        "total_found" : total_found,
                        "error" : None
                    },
                    "thing_data" : item
                }
        

        # If we made it this far something is wrong....
        return {
            "res_data" : {
                "thing" : None,
                "thing_time" : None,
                "total_found" : total_found,
                "error" : "Unknown error :("
            },
            "thing_data" : None
        }
            


if __name__ == "__main__":
    reddit = RedditSearch(secret.client_id, secret.client_secret, secret.user_agent, secret.device_id)
    reddit.get_token()
    # results = reddit.search(term = "luv", subreddit = "all", after = None, limit = 100, limit_to_sub = False, verbose = True)
    # for item in results["data"]["children"]:
    #     print(f"Name: {item['data']['name']} Sub: {item['data']['subreddit_name_prefixed']}@{helpers.readable_time(item['data']['created_utc'])}")