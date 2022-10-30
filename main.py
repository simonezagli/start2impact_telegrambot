#pyTelegramBotAPI
import telebot
import requests
import messages
import json
from datetime import datetime
from threading import Thread
import passwords


class User:

    def __init__(self, default_min_mc=0, default_max_mc=100000000000000000, default_message_status=False):
        """Initialize an instance of User class"""
        self.min_market_cap = default_min_mc
        self.max_market_cap = default_max_mc
        self.min_mc_status = False
        self.max_mc_status = False
        self.message_status = default_message_status

    def settings(self):
        """Return settings as a text"""
        text_html = f"\n<B>Settings</B>:" \
                    f"\nMax Market Cap: $ {self.max_market_cap}  (/set_max_market_cap)" \
                    f"\nMin Market Cap: $ {self.min_market_cap}  (/set_min_market_cap)"
        if self.message_status:
            text_html += f"\nDaily Message ENABLED (/daily_message)"
        else:
            text_html += f"\nDaily Message DISABLED (/daily_message)"
        return text_html


class MyThread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        """When time is 00:00, print start2impact report, save data into a json files and send report as message on
        telegram """
        while True:
            now = datetime.now()
            current_date = now.strftime("%m_%d_%Y")
            current_time = now.strftime("%H:%M:%S")
            if current_time == '00:00:00':
                data = get_start2impact_report(0)
                print(f"START2IMPACT REPORT of {current_date}" + data[1])
                with open('reports.json') as file:
                    reports = json.load(file)
                reports[f"{current_date}"] = data[2]
                with open("reports.json", "w") as outfile:
                    json.dump(reports, outfile)
                with open(f"{current_date}.json", "w") as outfile:
                    json.dump(data[3], outfile)
                send_daily_message(f"{current_date} {current_time}\n\n")


class Report:

    def __init__(self, chat_id):
        """Initialize an instance of Report class and get attributes"""
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': passwords.coinmarketcap_key}
        self.user_id = chat_id
        self.min_mc = database[self.user_id].min_market_cap
        self.max_mc = database[self.user_id].max_market_cap

    def get_data(self, params=None):
        """Return cryptocurrencies data"""
        r = requests.get(url=self.url, headers=self.headers, params=params).json()
        return r['data']

    def most_traded_24h(self, limit=1):
        """Return cryptocurrencies with the largest volume (in $) in the last 24 hours.
        It returns cryptocurrencies in json [0], html text [1], text [2] and it returns also also a list of symbols[3]
        Parameters: limit (min=1,max=5000).
        Default parameters: limit=1.
        MarketCap filter are defined by user settings"""
        currencies = self.get_data({
            'sort': 'volume_24h',
            'sort_dir': 'desc',
            'limit': limit,
            'market_cap_min': self.min_mc,
            'market_cap_max': self.max_mc})
        text_html = f"\n\n<b>Most Traded Cryptocurrency in last 24h</b>\n"
        text = "\n\nMost Traded Cryptocurrency in last 24h\n"
        symbols = []
        for currency in currencies:
            name = currency['name']
            symbol = currency['symbol']
            value = round(currency['quote']['USD']['volume_24h'], 2)
            text_html += f"<i>{name}</i> (/{symbol}) : $ {value} \n"
            text += f"{name} ({symbol}) : $ {value}\n"
            symbols.append(symbol)
        return currencies, text_html, text, symbols

    def best_price_change(self, time_lapse="24h", limit=10):
        """Return the best {limit} cryptocurrencies by percentage of price increase in the last {time_lapse}.
        It returns them in json [0], html text [1], text [2], and return also the time lapse [4] and a list
        of symbols[5].
        Parameters: time_lapse (24h, 7g, 30g), limit (min=1,max=5000).
        Default parameters: time_lapse=24h, limit=10.
        MarketCap filters are defined by user settings"""
        currencies = self.get_data({
            'sort': 'percent_change_' + time_lapse,
            'sort_dir': 'desc',
            'limit': limit,
            'market_cap_min': self.min_mc,
            'market_cap_max': self.max_mc})
        text_html = f"\n<b>Best Price Change in last {time_lapse}</b>\n"
        text = f"\nBest Price Change in last {time_lapse}\n"
        symbols = []
        for currency in currencies:
            name = currency['name']
            symbol = currency['symbol']
            value = round(currency['quote']['USD']['percent_change_24h'], 2)
            text_html += f"<i>{name}</i> (/{symbol}) : {value} %\n"
            text += f"{name} ({symbol}) : {value} %\n"
            symbols.append(symbol)
        return currencies, text_html, text, time_lapse, symbols

    def worst_price_change(self, time_lapse="24h", limit=10):
        """Return the worst {limit} cryptocurrencies by percentage price increase in the last {time_lapse}.
        It returns them in json [0], html text [1], text [2], and return also the time lapse [4] and a list
        of symbols[5].
        Parameters: time_lapse (24h, 7g, 30g), limit (min=1,max=5000).
        Default parameters: time_lapse=24h, limit=10.
        MarketCap filters are defined by user settings"""
        currencies = self.get_data({
            'sort': 'percent_change_' + time_lapse,
            'sort_dir': 'asc',
            'limit': limit,
            'market_cap_min': self.min_mc,
            'market_cap_max': self.max_mc})
        text_html = f"\n<b>Worst Price Change in last {time_lapse}</b>\n"
        text = f"\nWorst Price Change in last {time_lapse}\n"
        symbols = []
        for currency in currencies:
            name = currency['name']
            symbol = currency['symbol']
            value = round(currency['quote']['USD']['percent_change_24h'], 2)
            text_html += f"<i>{name}</i> (/{symbol}) : {value} %\n"
            text += f"{name} ({symbol}) : {value} %\n"
            symbols.append(symbol)
        return currencies, text_html, text, time_lapse, symbols

    def amount_to_buy_top(self, limit=20):
        """Return the amount needed to buy one coin of the top {limit} cryptocurrency by max market cap.
        Parameters: limit (min=1,max=5000).
        Default parameters: limit=20.
        MarketCap filters are defined by user settings
        It returns it in float [0], html text [1], text [2] and return also the limit [3]"""
        amount = 0
        currencies = self.get_data({
            'limit': limit,
            'market_cap_min': database[self.user_id].min_market_cap,
            'market_cap_max': database[self.user_id].max_market_cap})
        for currency in currencies:
            amount += currency['quote']['USD']['price']
        text_html = f"\n<b>Amount to buy top {limit} Currencies:</b> $ {round(amount, 4)}\n"
        text = f"\nAmount to buy top {limit} Currencies: $ {round(amount, 4)}\n"
        return round(amount, 4), text_html, text, limit

    def amount_to_buy_volume(self, volume=76000000):
        """Return the amount needed to buy one coin of all cryptocurrencies with a minimum volume.
        Parameters: volume (min=0,max=100000000000000000).
        Default volume value is 76 Million.
        MarketCap filters are defined by user settings
        It returns it in float [0], html text [1], text [2] and return also the volume [3]"""
        amount = 0
        currencies = self.get_data({
            'volume_24h_min': volume,
            'market_cap_min': database[self.user_id].min_market_cap,
            'market_cap_max': database[self.user_id].max_market_cap})
        for currency in currencies:
            amount += currency['quote']['USD']['price']
        text_html = f"\n<b>Amount to buy Currencies with 24h Volume over $ {volume}:</b> $ {round(amount, 4)}\n"
        text = f"\nAmount to buy Currencies with 24h Volume over {volume}: $ {round(amount, 4)}\n"
        return round(amount, 4), text_html, text, volume

    def gain_simulation_top_cryptocurrencies(self, limit=20):
        """Return gain or loss I could make
        if I buy one coin of every top {limit} market cap cryptocurrencies by max cap.
        MarketCap filters are defined by user settings
        It returns it in float [0], html text [1], text [2] and return also the limit [3]"""
        gain = 0
        currencies = self.get_data({
            'limit': limit,
            'market_cap_min': database[self.user_id].min_market_cap,
            'market_cap_max': database[self.user_id].max_market_cap})
        for currency in currencies:
            gain += currency['quote']['USD']['price'] - \
                     (currency['quote']['USD']['price'] / (1 + (currency['quote']['USD']['percent_change_24h'] / 100)))
        text_html = f"\n<b>Start2Impact Investment Simulation Gain or Loss:</b> $ {round(gain, 4)}\n"
        text = f"\nStart2Impact Investment Simulation Gain or Loss: $ {round(gain, 4)}\n"
        return round(gain, 4), text_html, text, limit

    def cryptocurrency_report(self, symbol):
        """Return currency data or False if the symbol isn't in the top 5000 cryptocurrencies on coinmarketcap"""
        # It can scan max 5000 cryptocurrencies
        data = self.get_data({'limit': '5000'})
        for currency in data:
            if currency['symbol'] == symbol:
                return currency
        return False


def new_user(chat_id):
    """Check if chat_id is present in database. If it isn't, make an instance of User and start backup_data function"""
    if chat_id not in database.keys():
        database[chat_id] = User()
        backup_data()


def check_status(message):
    """Check if a status is active when a command is called. If there is an active status,
     new command will be run instead of it"""
    if database[message.chat.id].min_mc_status and message.text[5:8] == 'min':
        return
    elif database[message.chat.id].max_mc_status and message.text[5:8] == 'max':
        return
    elif database[message.chat.id].min_mc_status:
        database[message.chat.id].min_mc_status = False
        bot.reply_to(message, f"Invalid value! Click /set_min_market_cap to try again")
    elif database[message.chat.id].max_mc_status:
        database[message.chat.id].max_mc_status = False
        bot.reply_to(message, f"Invalid value! Click /set_max_market_cap to try again")


def backup_data():
    """Make a Backup: save database data into backup.json"""
    for chat_id in database:
        backup[chat_id] = {
            'min_market_cap': database[chat_id].min_market_cap,
            'max_market_cap': database[chat_id].max_market_cap,
            'message_status': database[chat_id].message_status}
    with open("backup.json", "w") as outfile:
        json.dump(backup, outfile)


def set_min_market_cap(message):
    """Check input and change min market cap settings:
    Input must be a number lower than max market."""
    value = message.text
    if value.isdigit():
        value = float(message.text)
        if 100000000000000000 >= value < database[message.chat.id].max_market_cap:
            database[message.chat.id].min_mc_status = False
            database[message.chat.id].min_market_cap = value
            backup_data()
            bot.reply_to(message, f'Min market cap successfully sets at $ {database[message.chat.id].min_market_cap}$')
        else:
            bot.reply_to(message, f'Error: Min market cap must be lower than max market cap')
    else:
        check_status(message)


def set_max_market_cap(message):
    """Check input and change max market cap settings:
    Input must be a number between min market cap and 100000000000000000."""
    value = message.text
    if value.isdigit():
        value = float(message.text)
        if 100000000000000000 >= value > database[message.chat.id].min_market_cap:
            database[message.chat.id].max_mc_status = False
            database[message.chat.id].max_market_cap = value
            backup_data()
            bot.reply_to(message, f'Max market cap successfully sets at $ {database[message.chat.id].max_market_cap}$')
        else:
            if value < database[message.chat.id].min_market_cap:
                bot.reply_to(message, f'Error: Max market cap must be higher than min market cap')
            else:
                database[message.chat.id].max_market_cap = 100000000000000000
                bot.reply_to(message, f'Max market cap successfully sets at $ 100000000000000000 $')
    else:
        check_status(message)


def get_start2impact_report(chat_id):
    """Return start2impact report:
    The cryptocurrency with the largest volume (in $) in the last 24 hours
    The best and worst 10 cryptocurrencies (by percentage increase in the last 24 hours)
    The amount of money required to purchase one unit of each one of the top 20 cryptocurrencies
    in order of capitalization
    The amount of money required to purchase one unit of all cryptocurrencies whose last 24-hour volume
    exceeds $ 76,000,000
    The percentage of gain or loss you would have made if you had bought one unit of each one of the top
    20 cryptocurrencies, in order of capitalization of the past day (assuming the rank has not changed)
    It returns the report in html text [0], text [1], complete dict [2] and a compact dict [3]"""
    report = Report(chat_id)
    most_traded_24h = report.most_traded_24h()
    best_price_change = report.best_price_change()
    worst_price_change = report.worst_price_change()
    amount_to_buy_top = report.amount_to_buy_top()
    amount_to_buy_volume = report.amount_to_buy_volume()
    gain_simulation_top_cryptocurrencies = report.gain_simulation_top_cryptocurrencies()
    text_html = "<b>START2IMPACT REPORT</b>\n"
    text_html += database[chat_id].settings()
    text_html += most_traded_24h[1]
    text_html += best_price_change[1]
    text_html += worst_price_change[1]
    text_html += amount_to_buy_top[1]
    text_html += amount_to_buy_volume[1]
    text_html += gain_simulation_top_cryptocurrencies[1]
    text = most_traded_24h[2]
    text += best_price_change[2]
    text += worst_price_change[2]
    text += amount_to_buy_top[2]
    text += amount_to_buy_volume[2]
    text += gain_simulation_top_cryptocurrencies[2]
    report = {
        'most_traded_24h': most_traded_24h[0],
        f'best_price_change_{best_price_change[3]}': best_price_change[0],
        f'worst_price_change_{worst_price_change[3]}:': worst_price_change[0],
        f'amount_to_buy_top{amount_to_buy_top[3]}': amount_to_buy_top[0],
        f'amount_to_buy_volume{amount_to_buy_volume[3]}': amount_to_buy_volume[0],
        f'gain_simulation_top{gain_simulation_top_cryptocurrencies[3]}_cryptocurrencies':
            gain_simulation_top_cryptocurrencies[0]
    }
    compact_report = {
        'most_traded_24h': most_traded_24h[3],
        f'best_price_change_{best_price_change[3]}': best_price_change[4],
        f'worst_price_change_{worst_price_change[3]}:': worst_price_change[4],
        f'amount_to_buy_top{amount_to_buy_top[3]}': amount_to_buy_top[0],
        f'amount_to_buy_volume{amount_to_buy_volume[3]}': amount_to_buy_volume[0],
        f'gain_simulation_top{gain_simulation_top_cryptocurrencies[3]}_cryptocurrencies':
            gain_simulation_top_cryptocurrencies[0]
    }
    return text_html, text, report, compact_report


def symbol_report(message):
    """If text after '/' is a cryptocurrency symbol, return report, else send error message."""
    if message.text[0] == '/':
        report = Report(message.chat.id)
        currency = report.cryptocurrency_report(message.text[1:])
        if not currency:
            bot.reply_to(message, "This symbol is not present in our database, please try again with another one")
        else:
            bot.reply_to(message, messages.symbol(currency), parse_mode='HTML')


def send_daily_message(daily_info):
    """Send start2impact report to all users having 'daily message' enabled"""
    try:
        for chat_id in database:
            if database[chat_id].message_status and chat_id != "0":
                bot.send_message(chat_id, f"{daily_info}\n{get_start2impact_report(chat_id)[0]}", parse_mode='HTML')
    except RuntimeError:
        send_daily_message(daily_info)


bot = telebot.TeleBot(passwords.telegramBot_api_token)
backup = {}
database = {0: User()}  # 0 is the default user that makes reports without a call by user
thread_json = MyThread()


@bot.message_handler(commands=['start'])
def start(message):
    """Start chat, return intro message and start new_user function"""
    new_user(message.chat.id)
    check_status(message)
    mex = messages.start + messages.faq
    bot.send_message(message.chat.id, mex, parse_mode='HTML')


@bot.message_handler(commands=['set_min_market_cap'])
def set_min_market_cap_command(message):
    """Turn set_min_market_cap_status True and ask for min market cap"""
    check_status(message)
    database[message.chat.id].min_mc_status = True
    bot.send_message(message.chat.id, "Set Min Market Cap:")


@bot.message_handler(commands=['set_max_market_cap'])
def set_max_market_cap_command(message):
    """Turn set_max_market_cap_status True and ask for max market cap"""
    check_status(message)
    database[message.chat.id].max_mc_status = True
    bot.send_message(message.chat.id, "Set Max Market Cap:")


@bot.message_handler(commands=['start2impact_report'])
def start2impact_report(message):
    """In telegram chat, Return start2impact Report"""
    check_status(message)
    bot.reply_to(message, get_start2impact_report(message.chat.id)[0], parse_mode='HTML')


@bot.message_handler(commands=['settings'])
def settings_command(message):
    """In telegram chat, return user market cap settings"""
    check_status(message)
    bot.send_message(message.chat.id, database[message.chat.id].settings(), parse_mode='HTML')


@bot.message_handler(commands=['faq'])
def faq(message):
    """In telegram chat, return frequently asked question"""
    check_status(message)
    bot.send_message(message.chat.id, messages.faq, parse_mode='HTML')


@bot.message_handler(commands=['daily_message'])
def day_message(message):
    """Change message_status: enable/disable daily message"""
    if not database[message.chat.id].message_status:
        database[message.chat.id].message_status = True
        bot.send_message(message.chat.id, "Daily Message ENABLED")
        backup_data()
    else:
        database[message.chat.id].message_status = False
        bot.send_message(message.chat.id, "Daily Message DISABLED")
        backup_data()


@bot.message_handler(func=lambda m: True)
def message_scanner(message):
    """Scan message: if one of the market cap status are active, start set_market_cap function,
    else start symbol_report function"""
    if database[message.chat.id].min_mc_status:
        set_min_market_cap(message)
    elif database[message.chat.id].max_mc_status:
        set_max_market_cap(message)
    else:
        symbol_report(message)


# Import backup.json
with open('backup.json') as infile:
    users_backup = json.load(infile)
for user in users_backup:
    database[int(user)] = User(users_backup[user]['min_market_cap'],
                               users_backup[user]['max_market_cap'], users_backup[user]['message_status'])

thread_json.start()
try:
   bot.polling()
except requests.exceptions.ReadTimeout:
   bot.polling()

