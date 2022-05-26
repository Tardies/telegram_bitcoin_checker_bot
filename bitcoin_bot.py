import telebot
import requests
from time import sleep
from bs4 import BeautifulSoup
from datetime import datetime
bitcoin = 0.01301

def toFixed(numObj, digits=2):
    return f"{numObj:.{digits}f}"

bot = telebot.TeleBot("5374222900:AAHSy4EmHhQ2hVn3mQESxQKajeAGa71FA0U")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Type "/help"')

@bot.message_handler(commands=['help'])
def send_help(message):
    
    bot.reply_to(message, 'Use "/bitcoin_check" for one-time check\nUse "/bitcoin_check_infinite" for checking per up to 15 minutes')

@bot.message_handler(commands=['bitcoin_check'])
def send_bitcoin_check(message):
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
    bot.reply_to(message, output)

@bot.message_handler(commands=['bitcoin_check_infinite'])
def send_bitcoin_check_infinite(message):
    while True:
        now = datetime.now()
        current_time = int(now.strftime("%H"))
        if 6 < current_time and current_time < 23:
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
            bot.reply_to(message, output)
            sleep(60*15) #every 15 minutes
        else:
            output_arr = "Night time:\n"
            for _ in range(7):
                r = requests.get('https://crypto.com/price/bitcoin')
                soup = BeautifulSoup(r.content, 'html.parser')
                s = soup.find('h2', class_='chakra-heading css-64zram')
                content = s.find_all()
                c = str(content[1])
                c = c[39:48]
                c = c.replace(',', '')
                c = float(c)
                money = c * bitcoin
                time = now.strftime("%H:%M")
                output = f'{time}:\nCourse: ${c}\nBitcoins: {bitcoin}\nMoney: ${toFixed(money)}\n\n'
                output_arr += output
                sleep(60*60) #every hour
            bot.reply_to(message, output_arr)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)



bot.infinity_polling()