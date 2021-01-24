"""Basic Reddit API wrapper, provides search and search_until a datatime"""
import requests
import requests.auth
import Settings.secret as secret #!Remove once testing is complete
import Helpers.helpers as helpers

class RedditSearch():
    """This Reddit API wrapper, is bare bones and provides autherzation and search features only."""
    #TODO: Add __repr__()
    #TODO: Add token experation checker/updater

    def __init__(self, client_id, client_secret, user_agent, device_id):
        self.session_client = requests.Session()
        self.__URL = "https://oauth.reddit.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.device_id = device_id
        self.token = None
        self.token_type = None
        self.authorized = False
        self.total_searches = 0

        #*Update session headers
        self.session_client.headers.update({"User-Agent" : self.user_agent})

    def get_token(self):
        """Uses the 'Application Only OAuth' method to get a token from reddit.
        """
        auth_client = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        post_data = {
            "grant_type" : "https://oauth.reddit.com/grants/installed_client",
            "device_id" : self.device_id
        }

        res = self.session_client.post("https://www.reddit.com/api/v1/access_token", auth = auth_client, data = post_data)
        if res.status_code != requests.codes.ok:
            self.authorized = False
            return False

        # Extract token and access type from returned JSON
        j = res.json() #TODO Add Error Catch
        self.token = j["access_token"]
        self.token_type = j["token_type"]

        # Add auth to header
        self.session_client.headers.update({"Authorization" : f"{self.token_type} {self.token}"})
        self.authorized = True

        return True

    def search(self, term, subreddit = "all", limit = 25, limit_to_sub = False, sort = "new", nsfw = True, before = None, after = None, verbose = False):
        """Perform a basic search or slice of the given subreddit for the given term.
        limit can be between 0 and 100
        sort defaults to new can be one of ['relevance', 'hot', 'top', 'new', 'comments']
        verbose set to true will provide additonal console output.
        after/before must be set to a thing name - results are non inclusive"""
        # TODO: Add more error checking
        # TODO: Add rate limit checking
        self.total_searches += 1 # Just to keep track of session searches

        # Simple error check to limit 'limit' to okay values
        if limit > 100 or limit < 0:
            limit = 25

        # Check if sort is an okay value
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
        res = self.session_client.get(f"{self.__URL}/r/{subreddit}/search.json", params = params)

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
                "sent_headers" : res.request.headers,
                "rate_limit_used" : res.headers.get("x-ratelimit-used", None),
                "rate_limit_remain" : res.headers.get("x-ratelimit-remaining", None),
                "rate_limit_reset" : res.headers.get("x-ratelimit-reset", None),
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
            "sent_headers" : res.request.headers,
            "rate_limit_used" : res.headers.get("x-ratelimit-used", None),
            "rate_limit_remain" : res.headers.get("x-ratelimit-remaining", None),
            "rate_limit_reset" : res.headers.get("x-ratelimit-reset", None),
            "first_thing" : j['data']['children'][0]['data']['name'],
            "first_thing_created_utc" : j['data']['children'][0]['data']['created_utc'],
            "last_thing" : j['data']['children'][res_count - 1]['data']['name'],
            "last_thing_created_utc" : j['data']['children'][res_count - 1]['data']['created_utc']
        }

        # Debug Printing
        if verbose:
            # print(f"Generated URL: {j['res_data']['url']}")
            print(f"Rate Limit Used: {j['res_data']['rate_limit_used']}")
            print(f"Rate Limit Remain: {j['res_data']['rate_limit_remain']}")
            print(f"Rate Limit Reset: {j['res_data']['rate_limit_reset']}")
            # print(f"Response Headers: {j['res_data']['headers']}")
            # print(f"First Thing: {j['res_data']['first_thing']}")
            # print(f"Last Thing: {j['res_data']['last_thing']}")
            # print(f"Response Text: {res.text}")
            print(f"Results: {j['res_data']['count']}")

        return j

    def search_slice(self, term, subreddit, start_time, end_time, max_searches = 100, limit_to_sub = True, verbose = False):
        """This will perform several search_until calls to find the total number of things found
        for the given time window
        Expected Output;
        {
            "res_data" : {
                "thing" : "thingName", #* Name of thing or None if not found
                "total_found" : X, #* Sum total of all things that matched the search - valid even if max searches reached
                "error" : "error string" #* Human readable error string or None if no error
            }
        }"""

        # Start looking for start thing - as if we can't find that thing, no need to continue
        start_thing = self.search_until(term, subreddit, start_time, max_searches = max_searches, limit_to_sub = limit_to_sub, verbose = verbose)
        if start_thing['res_data']['error']:
            # Unable to find anything
            return {
                "res_data" : {
                    "thing" : None,
                    "total_found" : None,
                    "error" : "Unable to find a thing with start_time - search halted"
                }
            }
        end_thing = self.search_until(term, subreddit, end_time, after = start_thing['res_data']['thing'], max_searches = max_searches, limit_to_sub = limit_to_sub, verbose = verbose)
        if end_thing['res_data']['error']:
            return {
                "res_data" : {
                    "thing" : None,
                    "total_found" : None,
                    "error" : "Unable to find a thing with end_time - search halted"
                }
            }

        return end_thing

    def search_until(self, term, subreddit, until, after = None, max_searches = 100, limit_to_sub = True, nsfw = True, verbose = False):
        """
        Important note: Due to reddit limitations this function will often fail when searching for more than five days.
            It really depends on the subreddit and how much activity there is.
            I've had good results with no more than five days on r/all, thus I would think less active subs would
            work further back in time.
            It provides very little error checking so use at your own risk...
        Performs a normal search, until it finds a thing at the given datetime. If no item is found at the exact time of until
            it returns the next newest item, just inside of until.
        It then returns that thing name.
        Arguments:
            term: Search Term
            subreddit: Name of subreddit to search with no prefix i.e. 'all' or 'investing'
            until: string version of a datatime with format - '2021-01-01 12:00:00+0000'
            after: reddit thing name to search after
            max_searches: defaults to 100, make number of searches to perform
            limit_to_sub: defaults to True, limits searches to subbreddit
            nsfw: defaults to True, include NSFW results
            wiggle: defaults to 172800, number of seconds to look *past* until before giving up on search
            verbose: defaults to False - passed to search for verbose terminal output
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
        search_res = self.search(term = term, subreddit = subreddit, limit = max_searches, limit_to_sub = limit_to_sub, sort = "new", nsfw = nsfw, after = after, verbose = verbose)
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
            #TODO: Wiggle
            # Check if we found a thing as old OR older than we're looking for
            if search_res['res_data']['last_thing_created_utc'] <= until:
                found = True
            else:
                # Nothing found yet, do a new 'after' search
                total_found += search_res['res_data']['count'] # Add all found items to the count
                after_thing = search_res['res_data']['last_thing']
                search_res = self.search(term, subreddit, 100, True, after = after_thing, verbose = verbose)
                num_searches += 1

        # Loop to find the thing name that best matches our timeframe
        for i in range(search_res['res_data']['count']):
            return_item = None
            if search_res['data']['children'][i]['data']['created_utc'] > until:
                total_found += 1
            elif search_res['data']['children'][i]['data']['created_utc'] == until:
                # Wow what are the odds...
                return_item = search_res['data']['children'][i]
                total_found += 1
            elif search_res['data']['children'][i]['data']['created_utc'] <= until:
                # Found an item older than search time, return the item prior to it
                return_item = search_res['data']['children'][i-1]
                total_found += 1

            if return_item:
                # Build the return
                return {
                    "res_data" : {
                        "thing" : return_item['data']['name'],
                        "thing_time" : return_item['data']['created_utc'],
                        "searc_time" : until,
                        "thing_time_readable" : helpers.readable_time(return_item['data']['created_utc']),
                        "total_found" : total_found,
                        "error" : None
                    },
                    "thing_data" : return_item
                }


if __name__ == "__main__": #!Remove once testing is complete
    reddit = RedditSearch(secret.client_id, secret.client_secret, secret.user_agent, secret.device_id)
    reddit.get_token()
    results = reddit.search_until(term = "TSLA", subreddit = "investing", until = "2021-01-20 00:00:00+0000")
