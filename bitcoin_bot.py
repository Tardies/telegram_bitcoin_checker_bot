import telebot
import requests
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime

bitcoin = 0.01301
bot = telebot.TeleBot("") # paste your hash here

def toFixed(numObj, digits=2):
    return f"{numObj:.{digits}f}"

def bitcoin_scrap():
    r = requests.get('https://crypto.com/price/bitcoin')
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find('h2', class_='chakra-heading css-64zram')
    content = s.find_all()
    c = str(content[1])
    c = c[39:48]
    c = c.replace(',', '')
    c = float(c)
    money = c * bitcoin
    output = f'Course: ${c}\nBitcoins: {bitcoin}\nMoney: ${toFixed(money)}'
    return output

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Type "/help"')

@bot.message_handler(commands=['help'])
def send_help(message):
    
    bot.reply_to(message, 'Use "/bitcoin_check" for one-time check\nUse "/bitcoin_check_infinite" for checking per up to 15 minutes')

@bot.message_handler(commands=['bitcoin_check'])
def send_bitcoin_check(message):
    bot.reply_to(message, bitcoin_scrap())

@bot.message_handler(commands=['bitcoin_check_infinite'])
def send_bitcoin_check_infinite(message):
    while True:
        now = datetime.now()
        current_time = int(now.strftime("%H"))
        if 6 < current_time and current_time < 23:
            bot.reply_to(message, bitcoin_scrap())
            sleep(60*15) #every 15 minutes
        else:
            output_arr = "Night time:\n"
            for _ in range(7):
                time = now.strftime("%H:%M")
                output_arr += f'{time}:\n{bitcoin_scrap()}\n\n'
                sleep(2) #every hour
            bot.reply_to(message, output_arr)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)



bot.infinity_polling()
