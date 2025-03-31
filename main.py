import tweepy
import requests
import time
import os
from datetime import datetime

github_username = "nonbinarybyte"
github_repo = "Server25-OS"
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

def get_recent_commits():
    url = f"https://api.github.com/users/nonbinarybyte/events/public"
    response = requests.get(url)
    commits = []
    
    if response.status_code == 200:
        events = response.json()
        for event in events:
            if event["type"] == "PushEvent":
                for commit in event["payload"]["commits"]:
                    message = commit["message"]
                    commit_url = f"https://github.com/{github_username}/{github_repo}/commit/{commit['sha']}"
                    commits.append(f"- {message} ({commit_url})")
                break
    
    return "\n".join(commits[:3]) if commits else "No recent commits."

def tweet_update(api):
    image_path = os.path.join("ASSETS/IMG.jpg")
    status_text = f"Latest GitHub commits:\n{get_recent_commits()}\nMore at: https://github.com/{github_username} #devlog #indiedev #coding #developer #dev"
    
    try:
        api.update_status_with_media(status=status_text, filename=image_path)
        print(f"[{datetime.now()}] Tweet sent!")
    except Exception as e:
        print(f"Error posting tweet: {e}")

def main():
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)
    
    while True:
        tweet_update(api)
        time.sleep(3600)  # Wait 1 hour

if __name__ == "__main__":
    main()
