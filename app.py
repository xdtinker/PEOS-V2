import os
import telebot
import module_payload as cred
from flask import Flask, request
from peos import run as app
from pyngrok import ngrok


API_TOKEN = os.environ['API_TOKEN']

bot = telebot.TeleBot(API_TOKEN, parse_mode=None)
app = Flask(__name__)
https_tunnel = str(ngrok.connect("80", bind_tls=True)).split('"')[1]

bot = telebot.TeleBot(API_TOKEN)
bot.set_webhook(url=https_tunnel)
@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"

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
    bot.send_document(message.chat.id, open('certificate.pdf', 'rb'))
    os.remove('certificate.pdf')

if __name__ == "__main__":
    app.run(port=80)