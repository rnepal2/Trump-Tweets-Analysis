# standard libraries
import time
import json
# tweeter 
import tweepy

#Use your twitter API credentials ##SECRET## 
CONSUMER_KEY = " "
CONSUMER_SECRET = " "
ACCESS_KEY = " "
ACCESS_SECRET = " "


class TwitterBot:
    '''
    This is the TwitterBot class which has different methods designed to play with the 
    twitter API. The methods can perform the some of the tasks we can perform using 
    twitter application running those methods. 
    '''
    
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret):
        '''
        The constructor for TweetBot class.
        Parameters:
            twitter API credentials (SECRET): consumer_key, consumer_secret, access_key, access_secret
        Creates your twitter API object named api_.
        '''
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_key, access_secret)
        self.auth.secure = True
        self.api_ = tweepy.API(self.auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=True)

    @property
    def api(self):
        '''Returns the twitter API.'''
        return self.api_
    
    def user_timeline(self, user_screenname):
        '''
        Returns 20 most recent post on the user timeline.
            Parameters:
                screen_name of the user.
                example: string 'realDonaldTrump' given the twitter handle is: @realDonaldTrump
        '''
        timeline = self.api_.user_timeline(user_screenname, tweet_mode='extended')
        _list = list()
        for status in timeline:
            info = status._json
            _list.append({'time': info['created_at'], 'text': info['full_text']})
        return _list

    def user_followers(self, user_screenname):
        '''
        Returns the followers of a user (with name and screen name).
            Parameters:
                screen_name of the user.
        '''
        usr_followers = self.api_.followers(user_screenname)
        followers = list()
        for follower in usr_followers:
            followers.append({'name': follower._json['name'], 
                             'screen_name': follower._json['screen_name']})
        return followers

    def follow_user(self, user_screenname):
        '''
        This will make you follow a user.
            Parameteres:
                screen_name of the user you want to follow.
        '''
        confirm = input('Do you really want to follow %s? (Enter Y/N)' % user_screenname)
        confirm = confirm.lower()
        if confirm == 'n': return
        elif confirm == 'y':
            self.api_.create_friendship(user_screenname)
            print('You now follow @%s.' % user_screenname)
        else: print('Try again with a valid input.')
    
    def unfollow_user(self, user_screenname):
        '''
        This makes you unfollow an user.
            Parameters:
                screen_name of the user you want to unfollow.
        '''
        confirm = input('Do you really want to unfollow %s? (Enter Y/N)' % user_screenname).lower()
        if confirm == 'y':
            self.api_.destroy_friendship(user_screenname)
        elif confirm == 'n': return
        else: print('Enter a valid input.')
    
    def post_tweet(self, tweet_text):
        '''
        Posts a tweet in your timeline.
            Parameters:
                the text (string) of the tweet you want to post.
        '''
        self.api_.update_status(status=tweet_text)

    def reply_user(self, reply_text, user_screenname):
        '''
        Posts a tweet mentioning/replying an user.
            Parameters:
                reply: string, the text of the reply
                user_screenname: user screen_name to mention or reply
        '''
        self.api_.update_status(status=reply_text, user_screenname)
    
    # It returns the available information about a user given the screen_name.
    def user_info(self, user_screenname):
        '''
        Returns the information about a user: name, screen_name, description and location
            Parameters:
                screen_name of the user.
        '''
        user = self.api_.get_user(user_screenname)._json
        info = list()
        info.append({'name': user['name'], 'screen_name': user['screen_name'], 
                     'description': user['description'], 'location': user['location']})
        return info


if __name__ == "__main__":
    bot = TwitterBot(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
    print(bot.user_timeline('realDonaldTrump'))


'''
Ref: https://tweepy.readthedocs.io/en/v3.5.0/api.html#tweepy-api-twitter-api-wrapper
There are many more methods listed in the above Tweepy documentation, which can also be implemented here.
'''