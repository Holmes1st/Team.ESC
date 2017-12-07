class Type:
    AE = "2"
    CNT = "3"
    CI = "4"
    SUB = "23"


class CSE:
    host = '192.168.0.56'
    port = '7579'
    name = 'Mobius'
    id = '/Mobius'
    mqttport = 1883


class AE:
    host = "192.168.0.59"
    id = '/101'
    parent = CSE.id
    name = '101'
    appid = '101'
    port = '9727'
    bodytype = 'json'


cnt_arr = []

data = {}
data['parent'] = '/' + CSE.name + '/' + AE.name
data['name'] = 'cnt-camera'
cnt_arr.append(data)

