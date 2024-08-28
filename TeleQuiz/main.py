from telebot import TeleBot
import handlers

# Import the bot from the handlers module
bot = handlers.bot

def main():
    print("Bot is running...")
    bot.polling()

if __name__ == '__main__':
    main()
