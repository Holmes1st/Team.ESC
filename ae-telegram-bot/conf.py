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
    mqttport = '1883'


class AE:
    id = '/esc-bot'
    parent = CSE.id
    name = 'esc-bot'
    appid = 'esc-bot'
    port = '7580'
    bodytype = 'json'
