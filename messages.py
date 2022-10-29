def symbol(currency):
    """Return Cryptocurrency Report"""
    return f'''<b>-- {currency['symbol']} --</b>
<i>Price</i>: $ {currency['quote']['USD']['price']}  
<i>Volume 24h</i>: $ {round(currency['quote']['USD']['volume_24h'], 2)}  
<i>Volume %Change 24h</i>: {round(currency['quote']['USD']['volume_change_24h'], 2)} %  
<i>Price %Change 1h</i>: {round(currency['quote']['USD']['percent_change_1h'], 2)} %  {get_emoji(currency['quote']['USD']['percent_change_1h'])}
<i>Price %Change 24h</i>: {round(currency['quote']['USD']['percent_change_24h'], 2)} %  {get_emoji(currency['quote']['USD']['percent_change_24h'])}
<i>Price %Change 7d</i>: {round(currency['quote']['USD']['percent_change_7d'], 2)} %  {get_emoji(currency['quote']['USD']['percent_change_7d'])}
<i>Price %Change 30d</i>: {round(currency['quote']['USD']['percent_change_30d'], 2)} %  {get_emoji(currency['quote']['USD']['percent_change_30d'])}
<i>Price %Change 60d</i>: {round(currency['quote']['USD']['percent_change_60d'], 2)} %  {get_emoji(currency['quote']['USD']['percent_change_60d'])}
<i>Price %Change 90d</i>: {round(currency['quote']['USD']['percent_change_90d'], 2)} %  {get_emoji(currency['quote']['USD']['percent_change_90d'])}
<i>Market Cap</i>: $ {round(currency['quote']['USD']['market_cap'], 2)} 
<i>Fully Diluted Market Cap</i>: $ {round(currency['quote']['USD']['fully_diluted_market_cap'], 2)}'''


emoji = [(-75, '☠️'), (-50, '😱️'), (-25, '😰'), (-10, '☹️'), (0, '🙁'), (10, '😀'), (25, '😃'), (50, '😝'),
         (100, '💰')]


def get_emoji(n):
    for element in emoji:
        if float(n) < element[0]:
            return element[1]
    return '🚀'


start = '''🗣 <b>Start2impact Instant Reports 📈 </b> is a telegram bot that gives you instant updated reports.

<b>Commands</b>
/start 
/set_min_market_cap
/set_max_market_cap
/settings
/start2impact_report
/daily_message
/faq
/+ "CRYPTOCURRENCY SYMBOL"
'''

faq = '''
<b>FAQ</b>

Type <u>"/ + CRYPTOCURRENCY SYMBOL"</u> to receive the report of that specific cryptocurrency

For instance:
/BTC
/ETH
/BNB

<b>What is /start2impact_report?</b>
This is a report that returns you:
- best 10 cryptocurrencies for price change (%) in the last 24h
- worst 10 cryptocurrencies for price change (%) in the last 24h
- top currency for traded volume in the last 24h
- amount to buy top 20 cryptocurrencies by market cap
- amount to buy cryptocurrencies that have volume greater then 76 millions1
- simulation gains if yesterday I bought one coin of top20 cryptocurrencies by market cap

<b>What is /daily_message?</b>
When Enabled, start2impact report will be sent to you everyday at 00:00

<b>Setting</b>
You can personalize start2impact report setting min market cap with this command: /set_min_market_cap
Max market cap with this command: /set_max_market_cap 
Show your settings: /settings '''

