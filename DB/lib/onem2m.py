import json
import requests
import urllib.request
import socket
try:
    import shortid
except:
    import lib.shortid as shortid

base_headers = {}
base_headers['X-M2M-RI'] = ""
base_headers['Accept'] = "application/"
base_headers['X-M2M-Origin'] = ""

# base_headers['Locale'] = "en"


class createAE(object):
    """docstring for createAE."""

    def __init__(self, conf):
        super(createAE, self).__init__()
        self.headers = base_headers
        self.ae = conf.AE
        self.cse = conf.CSE

        self.body = {}
        self.body["m2m:ae"] = {}
        self.body["m2m:ae"]["rn"] = self.ae.name
        self.body["m2m:ae"]["api"] = self.ae.appid
        self.body["m2m:ae"]["rr"] = True
        self.body["m2m:ae"]["poa"] = ["http://" + self.ae.host + ":" + self.ae.port]

        self.bodyString = json.dumps(self.body)

        self.headers["X-M2M-RI"] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers['X-M2M-Origin'] = self.ae.id
        self.headers['Content-Type'] = 'application/vnd.onem2m-res+' + self.ae.bodytype + ";ty=" + conf.Type.AE
        self.headers['Content-Length'] = str(len(self.bodyString))

    def send(self):
        url = 'http://' + self.cse.host + ':' + self.cse.port + self.cse.id + '?rcn=3'
        # print("Try Create AE:", url)

        self.res = requests.post(url, data=self.bodyString, headers=self.headers)
        return self.res

        # if res.headers['X-M2M-RSC'] == '4105':
        #     print(res.headers['X-M2M-RSC'])
        #     print(res.text)
        #     return "crtae"
        #
        # elif res.headers['X-M2M-RSC'] in ['2001', '2000']:  # fail or success
        #     print(res.headers['X-M2M-RSC'], "Success", res.text['m2m:rce']['uri'])
        #     for key in data['m2m:rce']['m2m:ae'].keys():
        #         print(key + ":", data['m2m:rce']['m2m:ae'][key])
        #     return "crtcnt"
        #
        # elif res.headers['X-M2M-RSC'] == '5016':  # already exist
        #     print(res.headers['X-M2M-RSC'], res.text)
        #     return "rtvae"
        #
        # else:
        #     print(res.headers['X-M2M-RSC'], "Unknown")
        #     print(res.text)
        #     return "crtae"


class retrieveAE(object):
    """docstring for retrieveAE."""

    def __init__(self, conf):
        super(retrieveAE, self).__init__()
        self.cse = conf.CSE
        self.ae = conf.AE

        self.headers = base_headers
        self.headers["X-M2M-RI"] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers['X-M2M-Origin'] = self.ae.id

    def send(self):
        url = 'http://' + self.cse.host + ':' + self.cse.port + self.cse.id + self.ae.id
        self.res = requests.get(url, headers=self.headers)

        return self.res


class createCNT(object):
    """docstring for createCNT."""

    def __init__(self, conf, cnt):
        super(createCNT, self).__init__()
        self.cse = conf.CSE
        self.ae = conf.AE
        self.cnt = cnt

        self.body = {}
        self.body["m2m:cnt"] = {}
        self.body["m2m:cnt"]["rn"] = self.cnt['name']
        self.body["m2m:cnt"]["lbl"] = [self.cnt['name']]

        self.bodyString = json.dumps(self.body)

        self.headers = base_headers
        self.headers['X-M2M-RI'] = shortid.generate()
        self.headers['Accept'] += self.ae.bodytype
        self.headers["X-M2M-Origin"] = self.ae.id
        self.headers['Content-Type'] = 'application/vnd.onem2m-res+' + self.ae.bodytype + ";ty=" + conf.Type.CNT
        self.headers["Content-Length"] = str(len(self.bodyString))

    def send(self):
        url = "http://" + self.cse.host + ":" + self.cse.port + self.cnt["parent"] + '?rcn=3'
        self.res = requests.post(url, data=self.bodyString, headers=self.headers)

        return self.res


class createCI(object):
    """docstring for createCI."""

    def __init__(self, sender, target, con, bodytype="json", type="4"):
        super(createCI, self).__init__()
        self.url = target
        self.con = con

        self.body = {}
        self.body["m2m:cin"] = {}
        self.body["m2m:cin"]["con"] = con
        self.bodyString = json.dumps(self.body)

        self.headers = base_headers
        self.headers['X-M2M-RI'] = shortid.generate()
        self.headers["Accept"] += bodytype
        self.headers["X-M2M-Origin"] = sender
        self.headers['Content-Type'] = 'application/vnd.onem2m-res+' + bodytype + ";ty=" + type
        self.headers["Content-Length"] = str(len(self.bodyString))

    def send(self):
        url = "http://" + self.url
        self.res = requests.post(url, data=self.bodyString, headers=self.headers)

        return self.res


class createSUB(object):
    """docstring for createSUB."""

    def __init__(self, conf, sub):
        super(createSUB, self).__init__()
        self.conf = conf
        self.cse = conf.CSE
        self.ae = conf.AE
        self.sub = sub

        self.body = {}
        self.body["m2m:sub"] = {}
        self.body["m2m:sub"]["rn"] = self.sub["name"]
        self.body["m2m:sub"]["enc"] = {}
        self.body["m2m:sub"]["enc"]["net"] = [3]
        self.body["m2m:sub"]["nu"] = [self.sub['nu']]
        # self.body["m2m:sub"]["nct"] = 1
        self.bodyString = json.dumps(self.body)
        print(self.body)

        self.headers = base_headers
        self.headers['X-M2M-RI'] = shortid.generate()
        self.headers["Accept"] += self.ae.bodytype
        self.headers["X-M2M-Origin"] = self.ae.name
        self.headers['Content-Type'] = 'application/vnd.onem2m-res+' + self.ae.bodytype + ";ty=" + self.conf.Type.SUB
        self.headers["Content-Length"] = str(len(self.bodyString))

    def send(self):
        url = "http://" + self.cse.host + ":" + self.cse.port + "/Mobius/database-test/cnt-db"
        # print(url)
        self.res = requests.post(url, data=self.bodyString, headers=self.headers)
        return self.res


class deleteSUB(object):
    """docstring for deleteSUB."""

    def __init__(self, conf):
        super(deleteSUB, self).__init__()
        self.cse = conf.CSE
        self.ae = conf.AE

        self.headers = base_headers
        self.headers['Accept'] += self.ae.bodytype
        self.headers["X-M2M-Origin"] = self.ae.name
        self.headers['X-M2M-RI'] = shortid.generate()

    def send(self):
        url = "http://" + self.cse.host + ":" + self.cse.port + self.cse.id + self.ae.id + "/cnt-db/sub-db"
        print(url)
        # self.res = requests.delete(url, headers=self.headers)
        requests.delete(url, headers=self.headers)
        # self.req = urllib.request.Request(url=url, headers=self.headers, method='DELETE')
        # print("req Gened")
        # self.res = urllib.request.urlopen(self.req, timeout=5)
        print("res.fin")
        # return self.res
