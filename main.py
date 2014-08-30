import json
import urllib2
import Cookie
import requests
import sys

def get_session():
	response = urllib2.urlopen('https://pizzaonline.dominos.co.in/slot-machine/')
	headers = response.info()

	cookies = Cookie.SimpleCookie()
	cookies.load( headers['set-cookie'] )

	return cookies['session_id'].value

def get_coupon(session,myfile,success,failure):
	data = {'session_id':session}
	headers = {'X-Requested-With':'XMLHttpRequest'}
	response = requests.post('https://pizzaonline.dominos.co.in/slot-machine/process-slot.php',data=data,headers=headers)
	jsonResponse = json.loads(response.text)
	
	try:
		myfile.write('<tr><td>' + jsonResponse['unique_coupon'] + '</td>')
		myfile.write('<td>' + jsonResponse['coupon_description'] + '</td></tr>')
		success += 1
	except KeyError:
		failure += 1

	sys.stdout.write('success : '+str(success)+' , failures : '+str(failure)+'\r')
	sys.stdout.flush()

	if jsonResponse['status'] == 0:
		session = get_session()
	get_coupon(session,myfile,success,failure)		

def create_file():
	myfile = open('dominos_coupons.html','w+')
	myfile.write("<html><body><style>*{font-family:tahoma}</style><table border='1' cellspacing='0' cellpadding='10'>")
	return myfile


get_coupon(get_session(),create_file(),0,0)
