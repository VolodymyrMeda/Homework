from data_main import DataOperations
import telebot
from telebot import types

from emoji import emojize
import os
import datetime

TOKEN = '1154006871:AAGCBVC5bzmx4mZ2ftOwFzn99Lk6-bFFEA0'
base_url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
bot = telebot.TeleBot(TOKEN)

# collecting user's inputs
user_data = dict()
# starts time counting
time_start = datetime.datetime.now()
# spends control variable
spends = 0


@bot.message_handler(commands=['start'])
def start_handler(message):
    """
    Handles '/start' command, sends a message
    to the user with further instructions
    """
    bot.send_message(message.chat.id, f'Hello, I am going to help you a little in managing your money '
                                      f'{emojize(":wink:", use_aliases=True)} \n\n'
                                      f'/help - more info here')


@bot.message_handler(commands=['help'])
def help_handler(message):
    """
    Handles '/help' command, sends user
    the instructions how to use the bot
    """
    bot.send_message(message.chat.id, f'There are few things I will explain you '
                                      f'{emojize(":thinking_face:", use_aliases=True)}\n\n\n'
                                      '/spends - will allow you to control your spends \n\n'

                                      '*My spending* - the money you have spent\n\n'

                                      '*Spending in last time* - '
                                      'the money you have spent in certain period of time\n\n'

                                      '*Add spending* - allows you to add a certain amount of money you have spent\n\n'

                                      '*Reset* - sets all spends and time to zero\n\n\n\n'



                                      '/search - allows you to search for some products on ebay '
                                      'by the price you want\n\n'

                                      '*Enter the keyword of the product* - for example, \" Python for kids \" \n\n'

                                      'Then enter the price range you can afford to spend on the product\n\n'

                                      'I will return you *excel* and *pdf* files with info you need \n\n'
                                      'I have only chosen advertisements with free shipping, for your convenience '
                                      f'{emojize(":grinning:", use_aliases=True)}', parse_mode='Markdown')


@bot.message_handler(commands=['search'])
def search_handler(message):
    """
    Handles the '/search' command, runs the process
    of searching for the products, uses other functions
    for collecting data from user
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Find item on eBay')
    msg = bot.reply_to(message, 'Choose the option', reply_markup=markup)
    bot.register_next_step_handler(msg, keyword_handler)


@bot.message_handler(commands=['spends'])
def spends_handler(message):
    """
    Handles the '/spends' command, runs the
    process of working with user's spends
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('My spending', 'Spending in last time', 'Add spending', 'Reset')
    msg = bot.reply_to(message, 'Choose the option', reply_markup=markup)
    bot.register_next_step_handler(msg, spends_operations)


# spends control
def spends_operations(message):
    """
    All the actions with spends are handled here, depending
    on what user has chosen such action will happen

    'My spending' - returns the value user has spent
    'Spending in last time' - returns the value user has spent in certain period of time
    'Add spending' - allows user to add the value he spent, calls 'add_spend' function
    'Reset' - resets time and spends to zero

    'Back' - calls 'spends_handler'
    """
    global spends
    global time_start

    if message.text == 'My spending':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Back')
        msg = bot.reply_to(message, f'Your have spent - {spends} UAH', reply_markup=markup)
        bot.register_next_step_handler(msg, spends_handler)

    elif message.text == 'Spending in last time':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Back')
        now = datetime.datetime.now()
        duration = now - time_start
        msg = bot.reply_to(message, f'Your have spent - {spends} UAH in last {duration} hours', reply_markup=markup)
        bot.register_next_step_handler(msg, spends_handler)

    elif message.text == 'Add spending':
        msg = bot.send_message(message.from_user.id, 'How much did you spend?')
        bot.register_next_step_handler(msg, add_spend)

    elif message.text == 'Reset':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Back')
        spends = 0
        time_start = datetime.datetime.now()
        msg = bot.reply_to(message, f'Your spends have been set to 0, time counts from now', reply_markup=markup)
        bot.register_next_step_handler(msg, spends_handler)


def add_spend(message):
    """Adds the value user enters to all his spends"""
    global spends
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Back')
    try:
        spends += float(message.text)
        msg = bot.reply_to(message, f'{message.text} UAH added to your spends', reply_markup=markup)
    except ValueError:
        msg = bot.reply_to(message, f'You have entered something wrong '
                                    f'{emojize(":face_with_raised_eyebrow:", use_aliases=True)}', reply_markup=markup)

    bot.register_next_step_handler(msg, spends_handler)


# ebay search
def keyword_handler(message):
    """Gets a keyword of the product user wants to find"""
    if message.text == 'Find item on eBay':
        msg = bot.send_message(message.from_user.id, 'Enter the name of the item you want to find!')
        bot.register_next_step_handler(msg, price_from_handler)


def price_from_handler(message):
    """
    Saves the keywords user entered
    Gets a price range start value
    """
    user_data['keyword'] = message.text
    msg = bot.send_message(message.chat.id, 'Price from')
    bot.register_next_step_handler(msg, price_to_handler)


def price_to_handler(message):
    """
    Saves the price range start user entered
    Gets a price range end value
    """
    user_data['price_from'] = message.text
    msg = bot.send_message(message.chat.id, 'Price to')
    bot.register_next_step_handler(msg, result_return)


def result_return(message):
    """
    Saves the price range end user entered and does all the rest actions
    Uses data the user entered to make a request
    Returns 'results.xlsx' and 'results.pdf'
    """
    user_data['price_to'] = message.text

    data_operations = DataOperations()
    json_repr = data_operations.get_json_data(user_data['keyword'],
                                              user_data['price_from'],
                                              user_data['price_to'])
    try:
        data_operations.get_proper_data(json_repr)
        data_operations.data_excel_repr()
        data_operations.data_pdf_repr()

        file_excel = open('results.xlsx', 'rb')
        bot.send_document(message.from_user.id, file_excel)
        file_pdf = open('results.pdf', 'rb')
        bot.send_document(message.from_user.id, file_pdf)

        user_data.clear()
        os.remove('results.xlsx')
        os.remove('results.pdf')
    except TypeError:
        bot.send_message(message.chat.id, 'No results found by your request :(')


bot.polling()

if __name__ == '__main__':
    start_handler()
