from lib import logger
import requests,random,string
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

user_agent = 'Microsoft Office/16.0 (Windows NT 10.0; Microsoft Outlook 16.0.12026; Pro)'
headers = {'User-Agent': user_agent, 'Accept': 'application/json'}

def validate(email):
	try:
		r = requests.get('https://outlook.office365.com/autodiscover/autodiscover.json/v1.0/{}?Protocol=Autodiscoverv1'.format(email), headers=headers, verify=False, allow_redirects=False)
		if r.status_code == 200:
			logger.green('Verified: %s' % logger.GREEN(email))
			return True
		elif r.status_code == 302:
			if 'outlook.office365.com' not in r.text:
				logger.green('Verified: %s' % logger.GREEN(email))
				return True
			else:
				logger.verbose('Failed: %s' % logger.RED(email))
				return False
	except KeyboardInterrupt:
		logger.yellow('Keyboard interrupt detected!')
		quit()

def verify_o365(domain):
	logger.yellow('Attempting to verify if %s is using Office365' % logger.YELLOW(domain))
	domain_is_o365 = {}
	try:
		junk_user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
		r = requests.get('https://outlook.office365.com/autodiscover/autodiscover.json/v1.0/{}@{}?Protocol=Autodiscoverv1'.format(junk_user, domain), headers=headers, verify=False, allow_redirects=False)
		if 'outlook.office365.com' in r.text:
			logger.green('It looks like %s is using %s!' % (logger.GREEN(domain),logger.GREEN('Office365')))
			domain_is_o365[domain] = True
		else:
			logger.red('It doesnt look like %s is using %s' % (logger.RED(domain),logger.RED('Office365')))
			domain_is_o365[domain] = False
			quit()
	except Exception as e:
		logger.red(str(e))
		domain_is_o365[domain] = False
	print()
	return domain_is_o365