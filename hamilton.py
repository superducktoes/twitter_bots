import requests

class Hamilton:

    def __init__(self):
        self.data = requests.get("https://mario-blob-prod.azureedge.net/data/data-2.json").json()
        self.top_urls = self.data["breakoutUrls"]["data"]
        self.top_hashtags = self.data["breakoutHashtags"]["data"]
        
    def get_trending_urls(self):
        
        trending_urls = []

        for i in self.top_urls:
            trending_urls.append(i["name"])

        return trending_urls

    def get_trending_hashtags(self):

        trending_hashtags = []

        for i in self.top_hashtags:
            trending_hashtags.append(i["name"])


        return trending_hashtags
