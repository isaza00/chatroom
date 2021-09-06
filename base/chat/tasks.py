import requests
import re
import csv
import pika
from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message


API_URL = 'https://stooq.com/q/l/?s=stock_symbol.us&f=sd2t2ohlcv&h&e=csv'
ROW = 1
SYMBOL_COLUMN = 0
CLOSE_COLUMN = 6
STOCK_PATTERN = '/stock='
ERROR_MESSAGE = 'There is no data for requested symbol'

@shared_task
def send_bot_message(text_message, date, room_name):
    """ Process bot message, save it to db and send it to group """

    bot_message = get_bot_message(text_message)
    if not bot_message:
        return

    message = Message(
            user='BOT',
            text_message=bot_message,
            date=date,
            room=room_name)
    message.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_%s' % room_name,
        {
            'type': 'chat_message',
            'message': bot_message,
            'user': 'BOT',
            'date': date
        }
    )

def get_bot_message(text_message):
    """ Extract symbol from message and gets data """

    stock_symbol = None
    m = None
    bot_message = None
    
    m = re.search(f'^{STOCK_PATTERN}(\w+)', text_message)
    if m:
        stock_symbol = m.group(1)
    else:
        bot_message = f'{ERROR_MESSAGE}'
    if stock_symbol:
        bot_message = get_stock_data(stock_symbol)
    if not bot_message:
        bot_message = f'{ERROR_MESSAGE}'

    return bot_message

def get_stock_data(stock_symbol):
    """ Make the API call and process data """

    api_url = API_URL.replace('stock_symbol', stock_symbol)
    response = requests.get(api_url)
    if response.status_code == 200:
        decoded_content = response.content.decode('utf-8')
        csv_list = list(csv.reader(decoded_content.splitlines(), delimiter=','))
        close = csv_list[ROW][CLOSE_COLUMN]
        symbol = csv_list[ROW][SYMBOL_COLUMN]
        try:
            float(close)
            return f'{symbol} quote is ${close} per share'
        except:
            return None
    return None
