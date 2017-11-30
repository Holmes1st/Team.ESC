import conf
import json
import paho.mqtt.client as mqtt

import lib.onem2m as onem2m

status_flag = ["crtae", "rtvae", "crtcnt", "crtci", "ready"]


def DBAction(table, OC, userid):
    import lib.sqlaction as sqlaction

    db = sqlaction.DBAction(conf.DBServer.host, conf.DBServer.port, conf.DBServer.user, conf.DBServer.password)

    return db.defaultAction(table, OC, userid)


def mqttOnConnect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print("Listening At", "/oneM2M/req/Mobius/database-test/#")
    client.subscribe("/oneM2M/req/Mobius/database-test/#")


def mqttGotMessage(client, userdata, msg):
    print("Got message from", msg.topic)
    payload = json.loads(str(msg.payload, "utf8"))

    sender = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['cr']
    doorID = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['con'].split()[0]
    userid = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['con'].split()[1]

    try:  # 텔레그램봇에서 데이터 받았을 시 oc 값이 설정되어 있음
        OC = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['con'].split()[2]
    except:  # 문 ae 에서 데이터 받았을 시 oc값이 없음
        OC = "open"

    flag = DBAction(doorID, OC, userid)
    print(flag, type(flag))

    if flag == True:  # ok to open/close door

        # door control start
        url = conf.CSE.host + ":" + conf.CSE.port + conf.CSE.id + "/" + doorID + "/cnt-door"
        print(url)
        if OC == 'open':
            con = 1
        elif OC == 'close':
            con = 0
        else:
            return
            # con = 0  # 기존 상태 확인해서 기존 상태를 보내는 것도 괜찮을 듯
        res = onem2m.createCI(sender, url, con).send()
        for _ in range(10):
            if res.headers['X-M2M-RSC'] in ['2001', '2000']:
                break
            res = onem2m.createCI(sender, url, con).send()

        res_text = json.loads(res.text)
        print(res_text)
        # print(res.headers['X-M2M-RSC'], "Success")
        #
        # print("\n<---- created  content ---->")
        # for key in res_text['m2m:cin'].keys():
        #     print('    ' + key + ":", res_text['m2m:cin'][key])

        # door control finish

        # set led flag
        led = "1"

    else:  # not ok to open/close door
        # beep control start
        url = conf.CSE.host + ":" + conf.CSE.port + conf.CSE.id + "/" + doorID + "/cnt-buzz"
        print(url)
        con = "2"

        res = onem2m.createCI(sender, url, con).send()
        for _ in range(10):
            if res.headers['X-M2M-RSC'] in ['2001', '2000']:
                break
            res = onem2m.createCI(sender, url, con).send()

        print(res.headers['X-M2M-RSC'], "Success")

        res_text = json.loads(res.text)
        print(res_text)
        # print("\n<---- created  content ---->")
        # for key in res_text['m2m:cin'].keys():
        #     print('    ' + key + ":", res_text['m2m:cin'][key])
        # beep control finish

        # set led flag
        led = "2"

    # led control start
    url = conf.CSE.host + ":" + conf.CSE.port + conf.CSE.id + "/" + doorID + "/cnt-RGB"
    print(url)
    con = led

    res = onem2m.createCI(sender, url, con).send()
    for _ in range(10):
        if res.headers['X-M2M-RSC'] in ['2001', '2000']:
            break
        res = onem2m.createCI(sender, url, con).send()

    print(res.headers['X-M2M-RSC'], "Success")

    res_text = json.loads(res.text)
    print(res_text)
    # print("\n<---- created  content ---->")
    # for key in res_text['m2m:cin'].keys():
    #     print('    ' + key + ":", res_text['m2m:cin'][key])
    # led control finish


def mqttReady():
    client = mqtt.Client()
    client.on_connect = mqttOnConnect
    client.on_message = mqttGotMessage
    client.connect(conf.CSE.host, conf.CSE.mqttport, 60)

    client.loop_forever()


def crtae():
    print("Try: Create AE to CSE")

    res = onem2m.createAE(conf).send()
    res_text = json.loads(res.text)

    if res.headers['X-M2M-RSC'] in ['2001', '2000']:  # or success
        print(res.headers['X-M2M-RSC'], "Success", res_text['m2m:rce']['uri'])

        print("\n<------ created data ------>")
        for key in res_text['m2m:rce']['m2m:ae'].keys():
            print('    ' + key + ":", res_text['m2m:rce']['m2m:ae'][key])
        print("")

    elif res.headers['X-M2M-RSC'] == '4105':  # already exist
        print(res.headers['X-M2M-RSC'], res_text['m2m:dbg'])

    else:
        print(res.headers['X-M2M-RSC'], "Unknown")
        print(res.text)


def rtvae():
    print("Try: retrieve AE")

    res = onem2m.retrieveAE(conf).send()
    res_text = json.loads(res.text)

    if res.headers['X-M2M-RSC'] in ['2001', '2000']:  # success
        print(res.headers['X-M2M-RSC'], "Success", res_text['m2m:ae']['ri'])

        print("\n<-----  data from cse ----->")
        for key in res_text['m2m:ae'].keys():
            print('    ' + key + ":", res_text['m2m:ae'][key])
        print("")

    else:
        print(res.headers['X-M2M-RSC'], "Unknown")
        print(res_text['m2m:dbg'])


def crtcnt():
    for cnt in conf.cnt_arr:
        print("Try: create CNT - " + cnt['name'])
        res = onem2m.createCNT(conf, cnt).send()
        res_text = json.loads(res.text)

        if res.headers['X-M2M-RSC'] in ['2001', '2000']:  # success
            print(res.headers['X-M2M-RSC'], "Success", res_text['m2m:rce']['uri'])

            print("\n<------ created data ------>")
            for key in res_text['m2m:rce']['m2m:cnt'].keys():
                print('    ' + key + ":", res_text['m2m:rce']['m2m:ae'][key])
            print("")

        elif res.headers['X-M2M-RSC'] in ['4105']:  # success
            print(res.headers['X-M2M-RSC'], "Exist", res_text['m2m:dbg'])

        else:
            print(res.headers['X-M2M-RSC'], "Unknown")
            print(res_text['m2m:dbg'])


def crtci():
    url = conf.CSE.host + ":" + conf.CSE.port + conf.cnt_arr[0]["parent"] + "/" + conf.cnt_arr[0]['name']
    # url = conf.CSE.host + ":" + conf.CSE.port + "/thyme_test/cnt-led"
    print("Try: create CI -", url)

    res = onem2m.createCI(conf.AE.name, url, "None").send()
    res_text = json.loads(res.text)

    if res.headers['X-M2M-RSC'] in ["2000", "2001"]:
        print(res.headers['X-M2M-RSC'], "Success", res.headers['Content-Location'])

        print("\n<---- created  content ---->")
        for key in res_text['m2m:cin'].keys():
            print('    ' + key + ":", res_text['m2m:cin'][key])

    else:
        print(res.headers['X-M2M-RSC'], "Unknown", res_text['m2m:dbg'])
        print(res_text)


def crtSUB():
    res = onem2m.createSUB(conf, conf.sub_arr[0]).send()
    res_text = json.loads(res.text)

    print(res.headers['X-M2M-RSC'], res_text)


if __name__ == '__main__':
    crtae()
    crtcnt()
    crtci()
    crtSUB()
    mqttReady()
