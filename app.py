import os
import telebot
from flask import Flask, request
from pyngrok import ngrok
import re
import random
import requests
from bs4 import BeautifulSoup as bs

API_TOKEN = os.environ['API_TOKEN']

users = {}

bot = telebot.TeleBot(API_TOKEN, parse_mode=None)
_session = requests.Session()
app = Flask(__name__)
https_tunnel = str(ngrok.connect("80", bind_tls=True)).split('"')[1]

bot = telebot.TeleBot(API_TOKEN)
# bot.delete_webhook()
bot.set_webhook(url=https_tunnel)
@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"

class constants:
    def __init__(self) -> None:
        self._url = 'https://peos.dmw.gov.ph/controller/login.php'
        self._logout = 'https://peos.dmw.gov.ph/logout.php'
        self._patch_url = 'https://peos.dmw.gov.ph/hhw.php'
        self._module_url = 'https://peos.dmw.gov.ph/controller/selectQuestionsHHW.php'
        self._check_answer = 'https://peos.dmw.gov.ph/controller/checkAnswerHHW.php'
        self._get_cert = 'https://peos.dmw.gov.ph/controller/selectModuleHHW.php'
        self._fileLink = 'https://peos.dmw.gov.ph/peoshhwpdf.php'
class info():
    def __init__(self) -> None:
        self._id = ''
        self._lname = ''
        self._fname = ''
        self._type = ''

id = constants()
cred = info()

def payload(payload):
    _data = {
            '_login': {
                'eregno': cred._id,
                'lname': cred._lname,
                'fname': cred._fname,
                'type': cred._type,
                'token': '',
                'peos': 'peos'
            },

            1:{
                'm': 1,
                's': 1,
                'title': 'Module 1 | MAG AABROAD BA AKO O HINDI'
            },
            
            2:{
                'm': 2,
                's': 1,
                'title': 'Module 2 | PAANO MAG-APPLY'
            },
            3:{
                'm': 3,
                's': 1,
                'title': 'Module 3 | WORK ABROAD SAFELY'
            },
            4:{
                'm': 4,
                's': 1,
                'title': 'Module 4 | Anu-ano at Magkano ang mga Gagastusin sa Pag-a-apply?'
            },
            5:{
                'm': 5,
                's': 1,
                'title': 'Module 5 | Standard Employment Contract'
            },
            6:{
                'm': 6,
                's': 1,
                'title': 'Module 6 | Paano Mo Maaaring Ingatan ang Iyong Sarili sa Ibang Bansa?'
            },
            7:{
                'm': 7,
                's': 1,
                'title': 'Module 7 | POEA – Caring All The Way'
            },
            8:{
                'm': 8
            }
            }

    return _data[payload]



class User:  
    def __init__(self, userId, userName):  
        self.chat_id = userId  
        self.user_name = userName  

def _POST(html, key):
    _response = _session.post(html, data=key)
    return _response

def _PATCH(html):
    _response = _session.patch(html)
    return _response

def _GET(html):
    _response = _session.get(html)
    return _response

def _PARSE(html):
    _html = bs(html.content, "html.parser")
    return _html

def _verify(content):
    _noAccount = bool(re.search("<script>window.location.href = '../registerfirst.php'</script>", content)) 
    return _noAccount


@bot.message_handler(commands=['start', 'retry'])
def start(message):
    bot.send_message(message.chat.id, "Greetings! welcome to peos certificate generator to get started use /generate")
    bot.register_next_step_handler(message, getReg)

# @bot.message_handler(content_types = ['text'])
# def simple_response(message):
#     bot.send_message(users["{0}".format(users[message.chat.id][0])], text = users["{0}".format(users[message.chat.id][0])].first_name + ": " + message.text)

@bot.message_handler(commands=['generate'])
def getReg(message):
    data = User(message.chat.id, message.from_user.username)
    users[message.chat.id] = [data.chat_id, data.user_name]
    cred._lname=message.text
    bot.send_message(users[message.chat.id][0], "Enter your E-Registration number") 
    bot.register_next_step_handler(message, getLastname)

def getLastname(message):
        isNumber = message.text
        if not isNumber.isdigit():
            bot.reply_to(message, "E-Reg should be a number, try again. /generate")
            bot.register_next_step_handler(message, getReg)
            return
        cred._id = isNumber
        bot.send_message(users[message.chat.id][0], "What's your Last name?") 
        bot.register_next_step_handler(message, getFirstname)

def getFirstname(message):
    cred._lname=message.text
    bot.send_message(users[message.chat.id][0], "What's your first name?") 
    bot.register_next_step_handler(message, run)

def run(message):
    cred._fname=message.text
    bot.send_message(users[message.chat.id][0], "OK, please wait for a moment...")
    print(users)
    # login(message)

@bot.message_handler(commands=['override'])
def override(message):
    data = User(message.chat.id, message.from_user.username)
    users[message.chat.id] = [data.chat_id, data.user_name]
    bot.send_message(users[message.chat.id][0], "function override")
    print(users)
    login(message)

def login(message):
    print('ok')
    # Sending a POST request to the URL with the payload.
    _hasAccount = _POST(id._url, payload('_login'))

    if(_verify(_hasAccount.text)):
        bot.send_message(users[message.chat.id][0], 'No user found!')
    else:
        msg = bot.send_message(users[message.chat.id][0], 'user account validated!')
        bot.edit_message_text('please wait while I generate your certificate.', msg.chat.id, msg.message_id)
        _PATCH(id._patch_url)
        i = 0
        while i <= 7:
            i += 1
            if i == 8:
                _cert_content = _POST(id._get_cert, payload(i))
                _cert_parser = _PARSE(_cert_content)

                _certForm = _cert_parser.find_all('input')

                _CertID = _certForm[0].get('value')
                _CertName = _certForm[1].get('value')
                _certDate = _certForm[2].get('value')

                if message.chat.id in users:
                    bot.edit_message_text(f'👤 Name: {str(_CertName).upper()}\n🧾 CertID: {_CertID}\n📅 Issued Date: {_certDate}', msg.chat.id, msg.message_id)
                    _certFile = _GET(id._fileLink)

                    file_name = users[message.chat.id][1]+'.pdf'
                    with open(file_name, 'wb') as f:
                        f.write(_certFile.content)

                    bot.send_document(users[message.chat.id][0], open(file_name, 'rb'))
                    os.remove(file_name)
                else:
                    bot.send_message(users[message.chat.id][0], "Unique Identifier error") 
            else:
                html = _POST(id._module_url, payload(i))
                soup = _PARSE(html)
                parent = soup.find('form', { 'class': 'form' }).find_all('li')
                _ids = []
                for choices in parent:
                    _unique_ids = choices.find('input')
                    _ids.append(_unique_ids['name'])

                _payload = {
                            _ids[0]:random.choice(['tama','mali']),
                            _ids[1]:random.choice(['tama','mali']),
                            _ids[2]:random.choice(['tama','mali']),
                            _ids[3]:random.choice(['tama','mali']),
                            _ids[4]:random.choice(['tama','mali']),
                            'module':payload(i).get('m'),
                            'submodule':payload(i).get('s'),
                            'title':payload(i).get('title'),
                }

                _check_answer = _POST(id._check_answer, _payload)

                _isFailed = bool(re.search("Let's review again!", _check_answer.text))     

                if _isFailed:i-=1
                    # print(f'❗ Module {i} Status: ✓ FAILED')
                    # i-=1
                # else:
                #     print(f'🔰 Module {i} Status: ✓ PASSED')
                    # notification(f"[PASSED] {payload(i).get('title')}")
        _GET(id._logout)
        # bot.send_document(users[message.chat.id][0], open(f'{my_id}.pdf', 'rb'))
        # os.remove('{}.pdf'.format(my_id))
        # if my_id in session_id:session_id.remove(my_id)

if __name__ == "__main__":
    app.run(port=80)
