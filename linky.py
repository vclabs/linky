#!/usr/bin/python3
from lib import logger, core, banner, data_structure
import argparse, os.path, json
'''

Linky is a LinkedIn Enumerator.

Inspired by @vysecurity, built my @mez0cc.

'''

parser = argparse.ArgumentParser(description="Yet another LinkedIn scraper.",epilog="Example: python3 linky.py --cookie cookie.txt --company-id 1441 --domain google.com --output google_employees --format 'firstname.surname'")
mutually_exclusive = parser.add_mutually_exclusive_group()
parser.add_argument("-c", "--cookie", metavar="", help="Cookie to authenticate to LinkedIn with [li_at]")
parser.add_argument("-i", "--company-id", metavar="", help="Company ID number")
parser.add_argument("-k", "--keyword", metavar="", help="Keyword for searches")
parser.add_argument("-d", "--domain", metavar="", help="Company domain name")
parser.add_argument("-o", "--output", metavar="", help="File to output to: Writes CSV, JSON and HTML.")
parser.add_argument("-f", "--format", metavar="", help="Format for email addresses")
parser.add_argument("-v", "--validate", metavar="", help="Validate email addresses: O365/Hunter API")
parser.add_argument("-a", "--api", metavar="", help="API Key for Hunter API")
parser.add_argument("--verbose", action="store_true", help="API Key for Hunter API")
mutually_exclusive.add_argument("-V", "--version", action="store_true",help="Print current version")
args = parser.parse_args()

if args.version:
	banner.banner()
	quit()

# The most important part...
banner.banner()

if args.verbose:
	logger.verbose_switch = True

if args.cookie == None:
	logger.red('Please specify a file containing the %s cookie.' % logger.RED('li_at'))
	quit()

try:
	with open(args.cookie,'r') as f:
		cookie=f.readline().rstrip()
except:
	logger.red('Please add the cookie to a file')
	quit()

company_id=args.company_id

domain=args.domain

if args.output:
	filename = args.output
else:
	filename=None

if args.keyword == None:
	keyword = None
else:
	keyword = args.keyword

if args.format:
	email_schemes=['firstname.surname','firstnamesurname','f.surname','fsurname','surname.firstname','surnamefirstname','s.firstname','sfirstname']
	email_format=args.format.lower()
	if email_format not in email_schemes:
		logger.red('Unknown email scheme specified, please see the available below:')
		for i in email_schemes:
			logger.blue(i)
		quit()
else:
	email_format='firstname.surname'

if args.company_id == None:
	logger.red('Please specify a company id with the %s flag' % logger.RED('-i'))
	quit()
if args.domain == None:
	logger.red('Please specify a domain with the %s flag' % logger.RED('-d'))
	quit()

if args.validate:
	if args.validate.lower() == 'o365':
		validation = 'o365'
		api_key = None
	elif args.validate.lower() == 'hunter':
		if args.api == None:
			logger.red('If validating through Hunter, the API Key is required (%s).' % logger.RED('--api'))
			quit()
		else:
			api_key = args.api
		validation = 'hunter'

	else:
		logger.red('Unknown validation type: ' + logger.RED(args.validate))
		logger.red('Please specify either %s or %s' % (logger.RED('o365'),logger.RED('hunter')))
		quit()
else:
	validation = None
	api_key = None

data = data_structure.Data(cookie,company_id,email_format,domain,filename,keyword,validation,api_key)

for k,v in vars(data).items():
	if v != None:
		logger.blue('%s set to %s' % (k,logger.BLUE(v)))

try:
	users=core.run(data)
except KeyboardInterrupt:
	logger.yellow('Keyboard interrupt detected!')
	quit()

logger.green('Done!')