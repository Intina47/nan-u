# path: twitter_bot/twitter_manager.py
import datetime
import calendar
from .twitter_api import get_twitter_api

class TwitterManager:
    def __init__(self):
        self.api = get_twitter_api()
        self.tweets_count = 0

    def post_job(self, job):
        tweet_message = f"{job['title']} at {job['company']} - {job['location']} More info: {job['job_url']}"
        try:
            self.api.update_status(tweet_message)
            self.tweets_count += 1
            print("Tweet posted success.")
        except Exception as e:
            print(f"Failed to post tweet: {str(e)}")

    def can_post_today(self):
        today = datetime.date.today()
        _, num_days = calendar.monthrange(today.year, today.month)
        tweets_per_day = 1500 / num_days  # Average number of tweets per num_days
        days_left = num_days - today.day + 1

        return self.tweets_count < tweets_per_day * (today.day - 1)

    def reset_monthly_count(self):
        self.tweets_count = 0
