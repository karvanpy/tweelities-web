import os
import tweepy
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

def get_twitter_id(username):
    # Create a Tweepy API object
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create an API object
    api = tweepy.API(auth)

    if username.startswith('@'):
        username = username[1:]
        # Get the user object for the specified username
        user = api.get_user(screen_name=username)
        return user.id
    elif username.isdigit():
        user = api.get_user(user_id=username)
        return user.screen_name

@app.route('/', methods=['GET', 'POST'])
def index():
    twitter_username = ''
    twitter_id = ''
    compose_url = ''
    is_user_found = True
    is_id_found = True


    if request.method == 'POST':
        user_input = request.form['username']

        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        # Create an API object
        api = tweepy.API(auth)

        try:
            if user_input.startswith('@'):
                twitter_username = user_input[1:]
                twitter_id = api.get_user(screen_name=twitter_username).id
            elif not user_input.isdigit():
                twitter_username = user_input
                twitter_id = api.get_user(screen_name=twitter_username).id
            elif user_input.isdigit():
                twitter_id = user_input
                twitter_username = api.get_user(user_id=user_input).screen_name
            # is_user_found, is_id_found = True, True
            compose_url = "https://twitter.com/messages/compose?recipient_id={}".format(twitter_id)
        except tweepy.errors.NotFound as e:
            is_user_found, is_id_found = False, False
            return render_template('index.html', twitter_username=twitter_username, twitter_id=twitter_id, compose_url=compose_url, is_user_found=is_user_found, is_id_found=is_id_found)

    return render_template('index.html', twitter_username=twitter_username, twitter_id=twitter_id, compose_url=compose_url)

if __name__ == '__main__':
    app.run(debug=True)
