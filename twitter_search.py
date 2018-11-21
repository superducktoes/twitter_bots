import twitter
import json
import botometer
import config
from collections import Counter
import re

class Twitter_Search:

    def __init__(self, to_search):
        self.api = twitter.Api(consumer_key=config.consumer_key,
                               consumer_secret=config.consumer_secret,
                               access_token_key=config.access_token_key,
                               access_token_secret=config.access_token_secret)

        self.search_results = self.api.GetSearch(term=to_search, count=25)
        self.usernames = []
        self.full_account_information = []
        
    def get_raw_information(self):

        for i in self.search_results:
            account = {}
            account["username"] = i.user.screen_name
            account["profile_image_url"] = i.user.profile_image_url
            account["location"] = i.user.location
            account["created_at"] = i.user.created_at
            account["description"] = i.user.description
            if i.user.url:
                account["url"] = i.user.url
            account["tweet_count"] = str(i.user.statuses_count)
            account["retweet_count"] = str(i.retweet_count)
            account["followers_count"] = str(i.user.followers_count)
            self.full_account_information.append(account)

        return self.full_account_information

    def print_full_information(self):
        for i in self.search_results:
            print("\n=======================")
            print("Username: " + i.user.screen_name)
            if i.user.url:
                print("URL: " + i.user.url)
            print("Description: " + i.user.description)
            print("Profile Image URL: " + i.user.profile_image_url)
            print("Location: " + i.user.location)
            print("Created At: " + i.user.created_at)
            print("Tweet Count: " + str(i.user.statuses_count))
            print("Followers Count: " + str(i.user.followers_count))
            print("Retweet Count: " + str(i.retweet_count))
            print("\n")

    def get_usernames(self):
        
        for i in self.search_results:
            self.usernames.append(i.user.screen_name)

        return self.usernames

    def get_user_tweets(self):
        # later on get the first and last time stamp to see how much time between last x amount of tweets

        # create an empty dict to store the latest platform
        tweet_platform = []
        
        for i in self.search_results:

            # since the source has html tags we'll strip that away first
            source = re.search(">([^>]+)<", i.source).group()
            source = source[1:-1]
            tweet_platform.append(source)

            print("================")
            print("Tweet: " + i.text)
            print("Source: " + source)
            print("Created At: " + i.created_at)
            print("Hashtags: " + str(i.hashtags))
            print("User Mentions: " + str(i.user_mentions))
            print("\n")

        print("Tweet Stats:")
        print(Counter(tweet_platform))

        
    # eventually this needs to be moved to it's own class
    def bot_check(self):

        twitter_app_auth = {
            "consumer_key": config.consumer_key,
            "consumer_secret": config.consumer_secret,
            "access_token": config.access_token_key,
            "access_token_secret": config.access_token_secret
            }
        
        bom = botometer.Botometer(wait_on_ratelimit=True,
                                  mashape_key=config.mashape_key,
                                  **twitter_app_auth)
        counter = 0
        for i in self.full_account_information:
            bot_score = bom.check_account(i["username"])
            print("Username: " + i["username"])
            print("Bot Score(English): " + str(bot_score["display_scores"]["english"]))
            print("Bot Score(Universal): " + str(bot_score["display_scores"]["universal"]))
            print(self.full_account_information[counter])
            print("\n")
            counter = counter + 1
