import twitter
import json
import botometer
import config
from collections import Counter
import re
from bs4 import BeautifulSoup
import requests
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Twitter_Search:

    def __init__(self, to_search, limit):
        self.api = twitter.Api(consumer_key=config.consumer_key,
                               consumer_secret=config.consumer_secret,
                               access_token_key=config.access_token_key,
                               access_token_secret=config.access_token_secret)
        self.limit = limit
        self.search_results = self.api.GetSearch(term=to_search, count=limit)
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
        # get the screen name in case we want to check the bot score
        screen_name = ""
        
        tweet_count = 0
        retweet_count = 0
        
        for i in self.search_results:
            
            # since the source has html tags we'll strip that away first
            source = re.search(">([^>]+)<", i.source).group()
            source = source[1:-1]
            tweet_platform.append(source)

            print("================")
            if(i.text[:2] == "RT"):
                print("Tweet: " + i.text)
                retweet_count = retweet_count + 1
            else:
                tweet_count = tweet_count + 1
                print("\tTweet: " + i.text)
                
            print("Source: " + source)
            print("Created At: " + i.created_at)
            print("Hashtags: " + str(i.hashtags))
            print("User Mentions: " + str(i.user_mentions))
            print("\n")
            screen_name = i.user.screen_name

        user_choice = str(input("Check account's bot score? (y/n)"))
        if(user_choice.lower() == "y"):
            bot_score = self._get_bot_score(screen_name)
        else:
            bot_score = "N/A"
            
        print("Tweet Stats:")
        print(Counter(tweet_platform))
        print("Latest Tweet Date: " + self.search_results[0].created_at)
        print("Earliest Tweet Date: " + self.search_results[len(self.search_results)-1].created_at)
        print("Tweet Count: " + str(tweet_count))
        print("Retweet Count: " + str(retweet_count))
        
        # cast to str for bot score information
        print("Bot Score: " + str(bot_score))
        
    # eventually this needs to be moved to it's own class
    def bot_check(self):
        
        self._dedup_list()
        counter = 0
        # This checks the bot sentinel site and returns 1 if the user is found there and 0 if not
        #trollbot = self._get_trollbot_account(username)
        
        for i in self.full_account_information:
            print("Username: " + i["username"])
            print(self._get_bot_score(i["username"]))
            print(self._get_trollbot_account(i["username"]))
            print(self.full_account_information[counter])
            print("\n")
            counter = counter + 1

    def _get_bot_score(self, username):
        
        twitter_app_auth = {
            "consumer_key": config.consumer_key,
            "consumer_secret": config.consumer_secret,
            "access_token": config.access_token_key,
            "access_token_secret": config.access_token_secret
        }
        
        bom = botometer.Botometer(wait_on_ratelimit=True,
                                  mashape_key=config.mashape_key,
                                  **twitter_app_auth)
        
        score = bom.check_account(username)

        bot_score = {"Bot Score(English)" : score["display_scores"]["english"],
                     "Bot Score(Universal)" : score["display_scores"]["universal"]}
                  
        return bot_score

    def _get_trollbot_account(self,username):

        url_query = "https://botsentinel.com/category/all?s={}".format(username)
        trollbot_status = 0
        
        # make the request to bot sentinel
        r = requests.get(url_query, verify=False)

        # create bs object and search
        soup = BeautifulSoup(r.content, "html.parser")
        data = soup.find_all("div", class_="list-item dash-shadow-box")
        
        # check to see if we got back data we can actually use
        if data:
            data = str(data[0])

        # sleep since there's not an official api to call
        time.sleep(5)

        
        if "/category/trollbot" in data:
            trollbot_status = 1
        else:
            trollbot_status = 0

        return {"trollbot": trollbot_status}


    def _dedup_list(self):

        temp_list = []
        for i in self.full_account_information:
            if i["username"] not in temp_list:
                temp_list.append(i)

        self._full_account_information = temp_list
