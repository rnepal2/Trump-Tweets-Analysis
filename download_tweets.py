# standard libraries
import os, time
import json, tokenize

# tweeter 
import tweepy

###SECRET###
#Twitter API credentials  
CONSUMER_KEY = " "
CONSUMER_SECRET = " "
ACCESS_KEY = " "
ACCESS_SECRET = " "

class TweetLoader:
    '''
    creates an tweet loader object and loads the tweets of a user into a json file.
    '''
    def __init__(self, consumer_key, consumer_secret, access_key, access_secret, jsonfile=None):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_key, access_secret)
        self.auth.secure = True
        self.api_ = tweepy.API(self.auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=False)
        
        if jsonfile: self.jsonfile = jsonfile  
        else: self.jsonfile = 'saved_tweets.json'
    
    # returns the user API
    @property
    def api(self):
        return self.api_
    
    # collects tweet data and dumps into a json file
    # this collects upto 3200 latest tweets
    def tweet_collector(self, api, screen_name, jsonfile=None):
        '''collects tweets from a screen_name and saves into a json file'''
        tweets = tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items()
        
        file = open(self.jsonfile, 'w', encoding='utf-8')
        tweet_list = []; i = 0
        while True:
            try:
                tweet = next(tweets)
            except StopIteration:
                if i  > 3199:
                    print('Maximum API query limit reached!')
                else:
                    print('%d tweets from %s are loaded into the file!' %
                         (i, '@'+screen_name))
                break
            tweet_jsoned = json.dumps(tweet._json, sort_keys=True, indent=4, separators=(', ', ': '))
            tweet_dict = json.loads(tweet_jsoned)
            
            # saving only some important information of the tweet
            sub_dict_keys = ['full_text', 'created_at', 'is_retweet', 'retweet_count', 'favorite_count', 
                             'in_reply_to_user_id_str']
            
            sub_tweet = {x: tweet_dict[x] for x in sub_dict_keys if x in tweet_dict.keys()}
            
            tweet_list.append(sub_tweet.copy())
            i += 1
            
            if i % 400 == 0:
                #print('Sleeping for a minute!')
                #time.sleep(10)  # sleeping for a while to avoid maximum query hit.
                print('iterations: ', i)
                continue
        
        print('%d tweets are loaded into %s.' % (len(tweet_list), self.jsonfile))
        json.dump(tweet_list, file)
        file.close()

    # collects only 200 latest tweets
    # downloads the full 280 characters of the tweet.text
    def recent_tweets(self, api, screen_name, jsonfile=None):

        file = open(self.jsonfile, 'w', encoding='utf-8')
        tweet_list = []
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extended')

        sub_dict_keys = ['full_text', 'created_at', 'is_retweet', 'retweet_count', 'favorite_count', 
                         'in_reply_to_user_id_str']
        
        for i in range(len(new_tweets)):
            tweet = new_tweets[i]._json
            tweet_jsoned = json.dumps(tweet, sort_keys=True, indent=4, separators=(', ', ': '))
            tweet_dict = json.loads(tweet_jsoned)

            sub_tweet = {x: tweet_dict[x] for x in sub_dict_keys if x in tweet_dict.keys()}
            tweet_list.append(sub_tweet.copy())

        json.dump(tweet_list, file)
        file.close()
        print("recent %d tweets from %s are downloaded and saved in %s." % 
              (len(tweet_list), '@'+screen_name, self.jsonfile))


# user information 
screen_name = 'realDonaldTrump'  # President Trump's tweeter handle

# json file to save downloaded tweets
directory = './data'
if not os.path.exists(directory):
    os.makedirs(directory)
filename = os.path.join(directory, '2018-late.json')

# Downloading the tweets > .json file
def load_tweets(maximum_possible=True):
    loader = TweetLoader(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET, filename)
    api = loader.api_
    # if maximum possible: downloads upto 3200 tweets
    if maximum_possible:
        loader.tweet_collector(api, screen_name)
    # this downloads only recent 200 tweets
    else:
        loader.recent_tweets(api, screen_name)


# run?
if __name__ == "__main__":
    load_tweets()