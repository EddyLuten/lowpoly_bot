#!/usr/bin/env python3
import os
import sys
import tweepy
from time import sleep
from credentials import *

pid = str(os.getpid())
pidfile = '/tmp/lowpoly_bot.pid'

# Check if the process is already running, and if so, exit.
if os.path.isfile(pidfile):
    print('process already running, exiting...')
    sys.exit()

# If not, write the pid file
open(pidfile, 'w').write(pid)

def bot_main():
    tweet_interval = 20
    other_interval = 5

    # Access and authorize our Twitter credentials from credentials.py
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    import sqlite3
    conn = sqlite3.connect('./lowpoly_bot.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS processed (tweet_id UNSIGNED BIG INT)")
    conn.commit()

    spammers = open('./spammers', 'r').read().split(',')

    for tweet in tweepy.Cursor(api.search, q='#lowpoly -filter:retweets filter:media', result_type='recent').items():
        cursor = conn.cursor()

        if tweet.user.screen_name in spammers:
            print('Ignoring spammer ' + tweet.user.screen_name)
            continue

        cursor.execute('SELECT tweet_id FROM processed WHERE tweet_id = ?', (tweet.id,))
        if None is not cursor.fetchone():
            print('.', end='', flush=True)
            continue

        try:
            # Don't retweet retweets and quotes
            if tweet.retweeted or tweet.is_quote_status:
                continue

            # Retweet tweets as they are found
            tweet.retweet()
            print('Retweeted ' + str(tweet.id) + ' by ' + tweet.user.screen_name)

            cursor.execute('INSERT INTO processed (tweet_id) VALUES (?)', (tweet.id,))
            conn.commit()

            # Follow the user if we retweeted their stuff
            if not tweet.user.following:
                print('Followed ' + tweet.user.screen_name)
                tweet.user.follow()

            print('')
            sleep(tweet_interval)
        except tweepy.error.TweepError as e:
            print('Error (' + str(tweet.id) + '): ' + e.reason)

            if e.api_code == 429:
                print('Rate limited, pausing for 15 minutes.')
                sleep(15 * 60)
            else:
                cursor.execute('INSERT INTO processed (tweet_id) VALUES (?)', (tweet.id,))
                conn.commit()
                sleep(other_interval)

        except StopIteration:
            break

    conn.close()
    print('')

try:
    bot_main()
finally:
    os.unlink(pidfile)
