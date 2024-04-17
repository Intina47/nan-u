import tweepy

def get_twitter_api():
    consumer_key = ''  # API key
    consumer_secret = ''  # API secret key
    access_token = ''
    access_token_secret = ''
    
    # Correcting the class name for the OAuth handler
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    
    # Attempt to use the API to confirm authentication works
    try:
        api.verify_credentials()
        print("Successfully authenticated with Twitter API.")
    except tweepy.TweepyException as e:
        print(f"Failed to authenticate with Twitter API: {e}")
        return None  # Optionally return None or handle differently if auth fails
    
    return api

# Call the function to test authentication
api = get_twitter_api()
