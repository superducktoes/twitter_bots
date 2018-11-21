import requests

class Hamilton:

    def __init__(self):
        self.data = requests.get("https://mario-blob-prod.azureedge.net/data/data-2.json").json()
        self.top_urls = self.data["breakoutUrls"]["data"]
        
    def get_trending_urls(self):
        
        trending_urls = []

        for i in self.top_urls:
            trending_urls.append(i["name"])

        return trending_urls
