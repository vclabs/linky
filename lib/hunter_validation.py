# -*- coding: utf-8 -*-

import requests,  json, csv, argparse
from time import  sleep
from time import gmtime, strftime
from lib import logger

def validate(email,api_key):
	successful={}
	url='https://api.hunter.io/v2/email-verifier?email=%s&api_key=%s' % (email,api_key)
	try:
		r=requests.get(url)
		status_code = r.status_code
	except Exception as e:
		print(e)
		quit()

	try:
		data=json.loads(r.content)
	except Exception as e:
		print(e)
		quit()

	if status_code == 429 or status_code == 401:
		try:
			result=data['errors'][0]['details']
		except Exception as e:
			print(e)
			quit()

		if 'exceeded' in result:
			return 429
	
		elif 'No user found for the API key supplied' in result:
			return 401
	elif status_code == 200:
		try:
			result=data['data']['result']
			score=data['data']['score']
		except Exception as e:
			print(e)
			quit()

		percent=str(score)+'%'

		if score > 68:
			logger.verbose('Validated %s at %s' % (logger.GREEN(email),logger.GREEN(percent)))
			return True
		else:
			return False
	else:
		logger.verbose('Got unexpected HTTP response' % logger.RED(str(status_code)))