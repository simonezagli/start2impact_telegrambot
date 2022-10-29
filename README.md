# Start2Impact Python Project: Telegram bot for cryptocurrency reports

This bot was made to give people an opportunity to easily access instant cryptocurrencies reports through a simple chat interface on telegram.<br>

Every telegram chat with a bot has a /start command. Every time /start command is sent, it starts a function that checks if users that use the command is among the database of users; if not present, a new user was added. This database allows each users to have customized settings and, in case of down, restart the bot without problems.<br>

<b>SETTINGS</b><br>
Each user can customize his own market cap settings with the command /set_min_marketcap and /set_max_marketcap.<br>
When /set_min_marketcap and /set_max_marketcap are called, min/max market cap status is been active, and it is used to understand when a random message (no commands) refers to the setting of the market cap. <br><br>
Users can also enable/disable daily message: when enabled, a message with start2impact report will sent to you everyday at 00:00. (This function is not active on the online bot at the moment. It is in a beta status)

When a user calls /settings, a message with this user settings was returned

<b>REPORTS</b><br>
This bot allows to receive a preset report, called <b>start2impact report</b>, or specified cryptocurrencies report.<br>

1) <b>The first one is called with the command /start2impact_report and return:</b> <br>
- The cryptocurrency with the largest volume (in $) in the last 24 hours  <br>
- The best and worst 10 cryptocurrencies (by percentage increase in the last 24 hours)  <br>
- The amount of money required to purchase one unit of each one of the top 20 cryptocurrencies in order of capitalization  <br>
- The amount of money required to purchase one unit of all cryptocurrencies whose last 24-hour volume exceeds $ 76,000,000  <br>
- The percentage of gain or loss you would have made if you had bought one unit of each one of the top 20 cryptocurrencies, in order of capitalization of the past day (assuming the rank has not changed)  <br>
- Every day, at 00:00, this report is saved into reports.json file that collects everyday reports  <br>

2) <b>Cryptocurrency reports is called with "/Cryptocurrency Symbol" and return:</b><br>
- Price  <br>
- Volume 24h  <br>
- Volume %Change 24h  <br>
- Price %Change 1h  <br>
- Price %Change 24h  <br>
- Price %Change 7d  <br>
- Price %Change 30d  <br>
- Price %Change 60d  <br>
- Price %Change 90d  <br>
- Market Cap  <br>
- Fully Diluted Market Cap  <br><br>

Every day at 00:00, the bot saves start2impact report in two json files:.<br>
- reports.json
- a json file named with the current date of the report<br><br>

<b>For DEVELOPERS</b>:
- Python 2 or Python 3 is required.  <br>
- You have to install pyTelegramBotAPI: <br>
Install from source: <br>
$ git clone https://github.com/eternnoir/pyTelegramBotAPI.git <br>
$ cd pyTelegramBotAPI <br>
$ python setup.py install <br>
or install with pip: <br>
$ pip install pyTelegramBotAPI <br>

<b>LINKS</b>: 
- CoinMarketCap API: https://coinmarketcap.com/api/documentation/v1/ <br>
- pyTelegramBotAPI: https://github.com/eternnoir/pyTelegramBotAPI <br>
- Bot: https://t.me/start2impact_report_bot <br>


