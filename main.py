from gmail import GMail, Message
from alpha_vantage.timeseries import TimeSeries
from forex_python.converter import CurrencyRates
from time import sleep
import random
import requests
import schedule
import json
import os

# Hallo Lenny aus der Zukunft, ich weiß dieser Code ist der letzte Rotz. Doch ich habe echt keine Lust mehr,
# ich hoffe deine Augen bluten nicht. Grüß dein Vergangenheits Lenny

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"receiver": "", "mail": "", "password": ""}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

receiver = configData["receiver"]
mail = configData["mail"]
password = configData["password"]
api_key = configData["api_key"]


def get_tasks():
    tasks = ["read 20 pages", "learn english voc", "learn spanish voc", "train math exercises",
             "train chemistry exercises",
             "clean your room", "random wikipedia article", "30min programming in python",
             "10 min speed typing", "cook today", "SimpleClub", "Algorithms", "History Book", "play a Video Game"]
    your_tasks = random.sample(tasks, 3)
    return your_tasks




def get_stocks():
    c = CurrencyRates()
    eur = c.get_rate('USD', 'EUR')

    key = api_key
    ts = TimeSeries(key=key)

    taketwo_data = ts.get_quote_endpoint('TTWO')
    taketwo = taketwo_data[0]
    taketwo_price = round(float(taketwo['05. price']) * eur)
    taketwo_changes = round(float(taketwo['09. change']) * eur)

    jpmorgan_data = ts.get_quote_endpoint('JPM')
    jpmorgan = jpmorgan_data[0]
    jpmorgan_price = round(float(jpmorgan['05. price']) * eur)
    jpmorgan_changes = round(float(jpmorgan['09. change']) * eur)

    tencent_data = ts.get_quote_endpoint('TCEHY')
    tencent = tencent_data[0]
    tencent_price = round(float(tencent['05. price']) * eur)
    tencent_changes = round(float(tencent['09. change']) * eur)

    tesla_data = ts.get_quote_endpoint('TSLA')
    tesla = tesla_data[0]
    tesla_price = round(float(tesla['05. price']) * eur)
    tesla_changes = round(float(tesla['09. change']) * eur)

    apple_data = ts.get_quote_endpoint('AAPL')
    apple = apple_data[0]
    apple_price = round(float(apple['05. price']) * eur)
    apple_changes = round(float(apple['09. change']) * eur)

    return taketwo_price, taketwo_changes, jpmorgan_price, jpmorgan_changes, tencent_price, tencent_changes, tesla_price, \
           tesla_changes, apple_price, apple_changes


def get_quote():
    url = 'http://api.quotable.io/random'
    r = requests.get(url)
    quotes = r.json()
    quote = quotes['content']
    author = quotes['author']
    return quote, author


def send_email(recipient: str = receiver):
    quote = get_quote()
    stocks = get_stocks()
    tasks = get_tasks()

    content = f'''
Good Morning Mr. Warda
Have a nice day.\n
===========Task============
Your daily tasks are:
{tasks[0]}
{tasks[1]}
{tasks[2]}. \n
I know you will reach it.\n
=========Workout===========
Your workout overview for the week

Monday:
-10 Minutes sixpack Workout
-10 Minutes HIIT Workout

Tuesday:
-10 minutes chest workout
-10 minutes HIIT workout

Wednesday:
-20 Minutes HIIT Workout
-5 Minutes Biceps Workout

Thursday:
-7 Minutes sixpack Workout
-10 Minutes HIIT Workout

Friday:
-30 Minutes HIIT Workout

Saturday:
-20 Minutes HIIT Workout
-5 Minutes Chest Workout

Sunday:
-break
==========Stocks===========
Welcome to your daily stock overview:

TakeTwo's current price:
{stocks[0]}€
TakeTwo changed by
{stocks[1]}€
on the previous day

JPMorgan's current price:
{stocks[2]}€
JPMorgan changed by
{stocks[3]}€
on the previous day

Tencent's current price:
{stocks[4]}€
Tencent changed by
{stocks[5]}€
on the previous day

Tesla's current price:
{stocks[6]}€
Tesla changed by
{stocks[7]}€
on the previous day

Apple's current price:
{stocks[8]}€
Apple changed by
{stocks[9]}€
on the previous day\n

==========Quote===========
{quote[0]}
      -{quote[1]}
    '''

    gmail = GMail(f'Daily reminder{mail}', password=password)
    message = Message(f'Good Morning Mr. Warda', to=recipient, text=content)
    gmail.send(message)


if __name__ == '__main__':
    try:
        schedule.every().monday.at("08:00").do(send_email)
        schedule.every().tuesday.at("08:00").do(send_email)
        schedule.every().wednesday.at("08:00").do(send_email)
        schedule.every().thursday.at("08:00").do(send_email)
        schedule.every().friday.at("08:00").do(send_email)
        schedule.every().saturday.at("08:00").do(send_email)
        schedule.every().sunday.at("10:01").do(send_email)
    except:
        print("Not today")

    while True:
        schedule.run_pending()
        sleep(1)
