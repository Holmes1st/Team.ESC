class Type:
    AE = "2"
    CNT = "3"
    CI = "4"
    SUB = "23"


class DBServer:
    host = 'localhost'
    port = "3306"
    user = "root"
    password = 'root'


class CSE:
    host = 'localhost'
    port = '7579'
    name = 'Mobius'
    id = '/Mobius'
    mqttport = '1883'


class AE:
    id = '/database-test'
    parent = CSE.id
    name = 'database-test'
    appid = 'database-test'
    port = '9999'
    bodytype = 'json'


cnt_arr = []

data = {}
data['parent'] = '/' + CSE.name + '/' + AE.name
data['name'] = 'cnt-db'
cnt_arr.append(data)
