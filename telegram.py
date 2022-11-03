import telebot
import module_payload as cred
from peos import run as app
from constants import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

def process() -> None:
    @bot.message_handler(commands=['start', 'retry'])
    def start(message):
        bot.send_message(message.chat.id, "What's your E-Registration number?")
        bot.register_next_step_handler(message, getLastname)
        
    def getLastname(message):
        try:
            cred._id = int(message.text)
            bot.send_message(message.chat.id, "What's your Last name?") 
            bot.register_next_step_handler(message, getFirstname)
        except ValueError:
            bot.send_message(message.chat.id, 'Strings are not allowed in E-Reg number. Use /retry to try again.')  
        except Exception as e:
            print('error', e.with_traceback)

    def getFirstname(message):
        cred._lname=message.text
        bot.send_message(message.chat.id, "What's your first name?") 
        bot.register_next_step_handler(message, run)

    def run(message):
        cred._fname=message.text
        bot.send_message(message.chat.id, "OK, please wait for a moment...")
        app()

    bot.enable_save_next_step_handlers(delay=1)

    bot.load_next_step_handlers()

    bot.infinity_polling()
