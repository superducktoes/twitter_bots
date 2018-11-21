from hamilton import *
from twitter_search import *
import sys, os

def trending_urls():
    os.system("clear")
    data = Hamilton()
    trending_urls = data.get_trending_urls()
    for i in trending_urls:
        print(i)

    print("\n\n\n")
    return

def trending_hashtags():
    os.system("clear")
    data = Hamilton()
    trending_hashtags = data.get_trending_hashtags()

    for i in trending_hashtags:
        print(i)

if __name__ == "__main__":

    quit = False
    os.system("clear")
    print("Twitter Propaganda Bot Investigation")

    while quit == False:

        print("a. Trending URLs")
        print("b. Trending Hashtags")
        print("1. Twitter Search - full information(raw)")
        print("2. Twitter Search - full information(print)")
        print("3. Twitter Search - usernames only")
        print("4. Twitter Search - Auto Bot Check")
        print("5. Twitter Search - User Tweets")
        print("0. Quit")
        user_choice = str(input(">> "))
        
        try:
            if(user_choice.lower() == "a"):
                trending_urls()
                
            elif(user_choice.lower() == "b"):
                trending_hashtags()
                
            elif(user_choice == "1"):
                url = str(input("URL/Hashtag: "))
                limit = int(input("Limit: "))
                twitter_data = Twitter_Search(url, limit)
                full_twitter_data = twitter_data.get_raw_information()
                print(full_twitter_data)
                
            elif(user_choice == "2"):
                url = str(input("URL/Hashtag: "))
                limit = int(input("Limit: "))
                twitter_data = Twitter_Search(url, limit)
                full_twitter_data = twitter_data.print_full_information()

            elif(user_choice == "3"):
                url = str(input("URL/Hashtag: "))
                limit = int(input("Limit: "))
                twitter_data = Twitter_Search(url, limit)
                usernames = twitter_data.get_usernames()
                print(usernames)

            elif(user_choice == "4"):
                url = str(input("URL/Hashtag: "))
                limit = int(input("Limit: "))
                twitter_data = Twitter_Search(url, limit)
                full_twitter_data = twitter_data.get_raw_information()
                twitter_data.bot_check()
                
            elif(user_choice == "5"):
                username = str(input("Username: "))
                limit = int(input("Limit: "))
                # need to append from to exclude any re-tweets
                username = "from:" + username
                twitter_data = Twitter_Search(username, limit)
                tweets = twitter_data.get_user_tweets()
                
            elif(user_choice == "0"):
                quit = True
                sys.exit()
                
            else:
                "Please check your input"
        except Exception as e:
            print(e)
