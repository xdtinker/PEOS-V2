import os
import re
import random
import sys
import requests
from bs4 import BeautifulSoup as bs
from module_payload import payload
import constants as id

API_TOKEN = os.environ['API_KEY']

_session = requests.Session()
chat_id = 5336347826

# def _CREDENTIALS(cert,name,date):
#     _credentials = {
#         'cert_id': cert,
#         'name': name,
#         'date': date
#     }

#     return _credentials

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

def notification(msg):
    notify = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/sendMessage?chat_id={chat_id}&text={msg}')
    return notify

# <script>window.location.href = '../registerfirst.php'</script>

def _verify(content):
    _noAccount = bool(re.search("<script>window.location.href = '../registerfirst.php'</script>", content)) 
    return _noAccount

def login():
    # Sending a POST request to the URL with the payload.
    _hasAccount = _POST(id._url, payload('_login'))

    if(_verify(_hasAccount.text)):
        print('No user found!')
        sys.exit(0)
    else:
        print('user validated!')
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

                # notification(f'Certificate No.: {_cert_number}')
                # notification(f'Name: {_cert_name}')
                # notification(f'Issued Date: {_cert_date}')
                notification(f'👤 Name: {str(_CertName).upper()}\n🧾 CertID: {_CertID}\n📅 Issued Date: {_certDate}')
                print(f'Certificate No.: {_CertID}')
                print(f'Name: {_CertName}')
                print(f'Issued Date: {_certDate}')

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

                if _isFailed:
                    print('[FAILED]:',payload(i).get('title'))
                    i-=1
                else:
                    print('[PASSED]',payload(i).get('title'))
                    notification(f"[PASSED] {payload(i).get('title')}")

        _GET(id._logout)


def run() -> None:
    os.system('cls')
    login()
    print('Done')
