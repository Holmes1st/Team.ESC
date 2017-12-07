from SimpleCV import Color, Camera, Display
import lib.onem2m as onem2m
import time
import json
import conf

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


def crtci(result):
    url = conf.CSE.host + ":" + conf.CSE.port + "/Mobius/database-test/cnt-db" 
    # url = conf.CSE.host + ":" + conf.CSE.port + "/thyme_test/cnt-led"
    print("Try: create CI -", url)

    res = onem2m.createCI(conf.AE.name, url, conf.AE.name+' '+result).send()
    res_text = json.loads(res.text)

    if res.headers['X-M2M-RSC'] in ["2000", "2001"]:
        print(res.headers['X-M2M-RSC'], "Success", res.headers['Content-Location'])

        print("\n<---- created  content ---->")
        for key in res_text['m2m:cin'].keys():
            print('    ' + key + ":", res_text['m2m:cin'][key])

    else:
        print(res.headers['X-M2M-RSC'], "Unknown", res_text['m2m:dbg'])
        print(res_text)

def start():
	cam = Camera()
	display = Display()

	while(display.isNotDone()):

		img = cam.getImage()
	
		barcode = img.findBarcode()

		if(barcode is not None):
	

			barcode = barcode[0]
			temp = str(barcode.data)
			result = temp[10:18]
			crtci(result)
			time.sleep(3)
			barcode = []	
		
		

		img.save(display)


if __name__ == '__main__':
	crtcnt()
	start()
