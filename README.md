# lowpoly_bot

A now-dead Twitter bot written in Python 3 that used to post to this account: https://twitter.com/lowpoly_bot

The bot simply ran as a cron job every five minutes:

```
*/5 * * * * cd /root/bots/lowpoly_bot; /root/bots/lowpoly_bot/lowpoly_bot.py >> /var/log/lowpoly_bot.log 2>&1
```

It expects a file named `credentials.py` to be present with the following credentials obtained from Twitter:

```python
consumer_key = '<some string>'
consumer_secret = '<some string>'
access_token = '<some string>'
access_token_secret = '<some string>'
```

MIT Licensed.
