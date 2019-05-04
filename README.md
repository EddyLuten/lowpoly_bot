This ran in cron as:

```
*/5 * * * * cd /root/bots/lowpoly_bot; /root/bots/lowpoly_bot/lowpoly_bot.py >> /var/log/lowpoly_bot.log 2>&1
```
