import conf
import json
import paho.mqtt.client as mqtt

import lib.onem2m as onem2m
import lib.shortid as shortid

status_flag = ["crtae", "rtvae", "crtcnt", "crtci", "ready"]


def DBAction(table, OC, userid):
    import lib.sqlaction as sqlaction

    db = sqlaction.DBAction(conf.DBServer.host, conf.DBServer.port, conf.DBServer.user, conf.DBServer.password)

    return db.defaultAction(table, OC, userid)


def mqttOnConnect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print("Listening At", "/oneM2M/req/Mobius/database-test/#")
    client.subscribe("/oneM2M/req" + conf.CSE.id + conf.AE.id + "/#")


def mqttResponse(client, responseCode, to, fr, inpc):
    rsp_message = {}
    rsp_message['m2m:rsp'] = {}
    rsp_message['m2m:rsp']['rsc'] = responseCode
    rsp_message['m2m:rsp']['to'] = to
    rsp_message['m2m:rsp']['fr'] = fr
    rsp_message['m2m:rsp']['rqi'] = shortid.generate()
    rsp_message['m2m:rsp']['pc'] = ''
    client.publish("/oneM2M/resp" + conf.CSE.id + conf.AE.id + "/json", payload=json.dumps(rsp_message['m2m:rsp']))

def doorAction(OC, url):
    print("Ready to send cnt-door")
    if OC == "open":
        # open action
        print("Try : Create open Content to door")
        res = onem2m.createCI(conf.AE.name, url, 1).send()

    elif OC == "close":
        # close action
        print("Create close Content to door")
        res = onem2m.createCI(conf.AE.name, url, 2).send()

    # print response data
    print(res.headers)
    print(res.text)
    # try:
    #     if res.headers['X-M2M-RSC'] == '4105':
    #         print(res.headers['X-M2M-RSC'])
    #         print(res.text)
    #
    #     elif res.headers['X-M2M-RSC'] in ['2001', '2000']:  # fail or success
    #         print(res.headers['X-M2M-RSC'], "Success", res.text['m2m:rce']['uri'])
    #         for key in data['m2m:rce']['m2m:ae'].keys():
    #             print(key + ":", data['m2m:rce']['m2m:cnt'][key])
    #
    #     elif res.headers['X-M2M-RSC'] == '5016':  # already exist
    #         print(res.headers['X-M2M-RSC'], res.text)
    #
    #     else:
    #         print(res.headers['X-M2M-RSC'], "Unknown")
    #         print(res.text)
    # except Exception as e:
    #     print(e)

def buzzAction(flag, url):
    if flag == 1:
        # db action success
        print("Try : Create success Content to buzz")
        res = onem2m.createCI(conf.AE.name, url, 1).send()

    else:
        # db action fail
        print("Create fail Content to buzz")
        res = onem2m.createCI(conf.AE.name, url, 2).send()

    # print response data
    print(res.headers)
    print(res.text)
    # try:
    #     if res.headers['X-M2M-RSC'] == '4105':
    #         print(res.headers['X-M2M-RSC'])
    #         print(res.text)
    #
    #     elif res.headers['X-M2M-RSC'] in ['2001', '2000']:  # fail or success
    #         print(res.headers['X-M2M-RSC'], "Success", res.text['m2m:rce']['uri'])
    #         for key in data['m2m:rce']['m2m:ae'].keys():
    #             print(key + ":", data['m2m:rce']['m2m:cnt'][key])
    #
    #     elif res.headers['X-M2M-RSC'] == '5016':  # already exist
    #         print(res.headers['X-M2M-RSC'], res.text)
    #
    #     else:
    #         print(res.headers['X-M2M-RSC'], "Unknown")
    #         print(res.text)
    # except Exception as e:
    #     print(e)


def ledAction(flag, url):
    if flag == 1:
        # db action success
        print("Create success Content to led")
        res = onem2m.createCI(conf.AE.name, url, 1).send()

    else:
        # db action fail
        print("Create fail Content to led")
        res = onem2m.createCI(conf.AE.name, url, 2).send()

        # print response data
        print(res.headers)
        print(res.text)
        # try:
        #     if res.headers['X-M2M-RSC'] == '4105':
        #         print(res.headers['X-M2M-RSC'])
        #         print(res.text)
        #
        #     elif res.headers['X-M2M-RSC'] in ['2001', '2000']:  # fail or success
        #         print(res.headers['X-M2M-RSC'], "Success", res.text['m2m:rce']['uri'])
        #         for key in data['m2m:rce']['m2m:ae'].keys():
        #             print(key + ":", data['m2m:rce']['m2m:cnt'][key])
        #
        #     elif res.headers['X-M2M-RSC'] == '5016':  # already exist
        #         print(res.headers['X-M2M-RSC'], res.text)
        #
        #     else:
        #         print(res.headers['X-M2M-RSC'], "Unknown")
        #         print(res.text)
        # except Exception as e:
        #     print(e)


def mqttGotMessage(client, userdata, msg):
    print("Got message from", msg.topic)
    payload = json.loads(str(msg.payload, "utf8"))

    mqttResponse(client, 2001, '', conf.AE.name, '')

    sender = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['cr']
    doorID = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['con'].split()[0]
    userid = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['con'].split()[1]

    try:  # 텔레그램봇에서 데이터 받았을 시 oc 값이 설정되어 있음
        OC = payload['pc']['m2m:sgn']['nev']['rep']['m2m:cin']['con'].split()[2]
    except:  # 문 ae 에서 데이터 받았을 시 oc값이 없음
        OC = "open"

    flag = DBAction(doorID, OC, userid)
    print(flag, type(flag))

    doorUrl = conf.CSE.host + ":" + conf.CSE.port + '/' + conf.CSE.name + '/' + doorID + '/cnt-door'
    ledUrl = conf.CSE.host + ":" + conf.CSE.port + '/' + conf.CSE.name + '/' + doorID + '/cnt-RGB'
    buzzUrl = conf.CSE.host + ":" + conf.CSE.port + '/' + conf.CSE.name + '/' + doorID + '/cnt-buzz'

    if flag:
        doorAction(OC, doorUrl)
        ledAction(1, ledUrl)
        buzzAction(1, buzzUrl)

    else:
        ledAction(2, ledUrl)
        buzzAction(2, buzzUrl)


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
                print('    ' + key + ":", res_text['m2m:rce']['m2m:cnt'][key])
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


def delSUB():
    res = onem2m.deleteSUB(conf).send()

    print(res.headers)
    print(res.text)


def crtSUB():
    res = onem2m.createSUB(conf, conf.sub_arr[0]).send()
    res_text = json.loads(res.text)

    print(res.headers['X-M2M-RSC'], res_text)


if __name__ == '__main__':
    import time
    crtae()
    time.sleep(1)
    crtcnt()
    time.sleep(1)
    # delSUB()
    time.sleep(1)
    crtSUB()
    time.sleep(1)
    mqttReady()
