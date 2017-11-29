import conf
import json

import lib.onem2m as onem2m

status_flag = ["crtae", "rtvae", "crtcnt", "crtci", "ready"]


def DBAction():
    try:
        import lib.sqlaction as sqlaction
    except:
        import sqlaction

    db = sqlaction.DBAction(conf.DBServer.host, conf.DBServer.port, conf.DBServer.user, conf.DBServer.password)


def mqttOnConnect():
    pass


def mqttGotMessage():
    pass


def mqttReady():
    import paho.mqtt.client as mqtt

    client = mqtt.Client()
    client.on_connect = mqttOnConnect
    client.on_message = mqttGotMessage
    client.connect(conf.CSE.host, conf.CSE.mqttport, 60)

    client.loop_forever()


if __name__ == '__main__':
    status = status_flag[3]

    if status == status_flag[0]:  # crtae
        print("Try: Create AE to CSE")

        res = onem2m.createAE(conf).send()
        res_text = json.loads(res.text)

        if res.headers['X-M2M-RSC'] in ['2001', '2000']:  # or success
            print(res.headers['X-M2M-RSC'], "Success", res_text['m2m:rce']['uri'])

            print("\n<------ created data ------>")
            for key in res_text['m2m:rce']['m2m:ae'].keys():
                print('    ' + key + ":", res_text['m2m:rce']['m2m:ae'][key])

            status = "crtcnt"

        elif res.headers['X-M2M-RSC'] == '4105':  # already exist
            print(res.headers['X-M2M-RSC'], res_text['m2m:dbg'])
            status = "rtvae"

        else:
            print(res.headers['X-M2M-RSC'], "Unknown")
            print(res.text)
            status = "crtae"

    elif status == status_flag[1]:  # rtvae
        print("Try: retrieve AE")

        res = onem2m.retrieveAE(conf).send()
        res_text = json.loads(res.text)

        if res.headers['X-M2M-RSC'] in ['2001', '2000']:  # success
            print(res.headers['X-M2M-RSC'], "Success", res_text['m2m:ae']['ri'])

            print("\n<-----  data from cse ----->")
            for key in res_text['m2m:ae'].keys():
                print('    ' + key + ":", res_text['m2m:ae'][key])
            status = "crtcnt"

        else:
            print(res.headers['X-M2M-RSC'], "Unknown")
            print(res_text['m2m:dbg'])
            status = "crtae"

    elif status == status_flag[2]:  # crtcnt
        for cnt in conf.cnt_arr:
            print("Try: create CNT - " + cnt['name'])
            res = onem2m.createCNT(conf, cnt).send()
            res_text = json.loads(res.text)

            if res.headers['X-M2M-RSC'] in ['2001', '2000']:  # success
                print(res.headers['X-M2M-RSC'], "Success", res_text['m2m:rce']['uri'])

                print("\n<------ created data ------>")
                for key in res_text['m2m:rce']['m2m:ae'].keys():
                    print('    ' + key + ":", res_text['m2m:rce']['m2m:ae'][key])
                status = "crtci"

            else:
                print(res.headers['X-M2M-RSC'], "Unknown")
                print(res_text['m2m:dbg'])

    elif status == status_flag[3]:  # crtci
        # url = conf.CSE.host + ":" + conf.CSE.port + conf.cnt_arr[0]["parent"] + "/" + conf.cnt_arr[0]['name']
        url = conf.CSE.host + ":" + conf.CSE.port + "/thyme_test/cnt-led"
        print("Try: create CI -", url)

        res = onem2m.createCI(conf.AE.name, url, "None").send()
        res_text = json.loads(res.text)

        if res.headers['X-M2M-RSC'] in ["2000", "2001"]:
            print(res.headers['X-M2M-RSC'], "Success", res.headers['Content-Location'])

            print("\n<---- created  content ---->")
            for key in res_text['m2m:cin'].keys():
                print('    ' + key + ":", res_text['m2m:cin'][key])

            status = "ready"
        else:
            print(res.headers['X-M2M-RSC'], "Unknown", res_text['m2m:dbg'])
            print(res_text)

    else:
        pass
