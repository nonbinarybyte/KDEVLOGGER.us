import tweepy
import requests
import time
import os
from datetime import datetime

github_username = "nonbinarybyte"
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

def get_recent_commits():
    repos_url = f"https://api.github.com/users/{github_username}/repos"
    repos_response = requests.get(repos_url)
    commits = []
    
    if repos_response.status_code == 200:
        repos = repos_response.json()
        for repo in repos:
            repo_name = repo["name"]
            commits_url = f"https://api.github.com/repos/{github_username}/{repo_name}/commits"
            commits_response = requests.get(commits_url)
            
            if commits_response.status_code == 200:
                repo_commits = commits_response.json()
                for commit in repo_commits[:3]:  # Get latest 3 commits per repo
                    message = commit["commit"]["message"]
                    commit_url = commit["html_url"]
                    commits.append(f"[{repo_name}] {message} ({commit_url})")
    
    return "\n".join(commits[:5]) if commits else "No recent commits."

def tweet_update(api):
    image_path = os.path.join("ASSETS/IMG.jpeg")
    status_text = f"Latest GitHub commits:\n{get_recent_commits()}\nMore at: https://github.com/{github_username}"
    
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
