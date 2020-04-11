import tweepy
CONSUMER_KEY = 'X7HZ0q5cHDflirTzHkF49hPXF'
CONSUMER_SECRET = 'XBaDIPMZoIZ2c60qTx6QVAWz65qglBKy0zGxsilLnrDEm9yPY7 '

def get_api(request):

    oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    access_key = oauth.access_token
    access_secret = oauth.access_token_secret
    oauth.set_access_token(access_key, access_secret)
    api = tweepy.API(oauth)
    return api
