
# _id = '2022110337989'
# _lname = 'michelk'
# _fname = 'john'
# _type = 2

_id = ''
_lname = ''
_fname = ''
_type = 2

def payload(payload):
    _data = {
            '_login': {
                'eregno': _id,
                'lname': _lname,
                'fname': _fname,
                'type': _type,
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
