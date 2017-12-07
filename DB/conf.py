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
    host = "192.168.0.52"
    id = '/database-test'
    parent = CSE.id
    name = 'database-test'
    appid = 'database-test'
    port = '9999'
    bodytype = 'json'

class DBServer:
    host = CSE.host
    port = "3306"
    user = "root"
    password = 'root'

cnt_arr = []

data = {}
data['parent'] = '/' + CSE.name + '/' + AE.name
data['name'] = 'cnt-db'
cnt_arr.append(data)

sub_arr = []

data = {}
data['parent'] = '/' + CSE.name + '/' + AE.name + '/' + cnt_arr[0]['name']
data['name'] = "sub-db"
data['nu'] = "mqtt://" + CSE.host + AE.id + '?ct=' + AE.bodytype
sub_arr.append(data)
