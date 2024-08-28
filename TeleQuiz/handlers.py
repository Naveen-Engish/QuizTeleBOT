from telebot import TeleBot
from timer import Timer
from registration import register_leader,handle_callback

# Initialize the bot and the timer
bot = TeleBot('7203587973:AAGEYfH-VaZB_pyNj0BECl0Z2nDiSArGSCo')
timer = Timer()

# Command handler for /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Timer has already started!")
    bot.reply_to(message, f"Time left: {timer.time_left()}")
    register_leader(message, bot)

# Command handler for /time
@bot.message_handler(commands=['time'])
def time(message):
    bot.reply_to(message, timer.time_left())

# Handle callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    handle_callback(call, bot)



