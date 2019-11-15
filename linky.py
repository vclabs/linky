#!/usr/bin/python3
from lib import logger, core, banner, data_structure, naming_scheme
import argparse, os.path, json, datetime

'''

Linky is a LinkedIn Enumerator.

Inspired by @vysecurity, built my @mez0cc.

'''

start_time = datetime.datetime.now().replace(microsecond=0)

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
parser.add_argument("-t", "--threads", metavar="", help="Amount of threads to use [default 5]")
parser.add_argument("--valid-emails-only", action="store_true", help="When you literally only want a txt of valid emails.")
parser.add_argument("--verbose", action="store_true", help="Verbosity of the output")
parser.add_argument("--debug", action="store_true", help="Enable debugging, will spam.")
mutually_exclusive.add_argument("--list-email-schemes", action="store_true", help="List available email schemes")
mutually_exclusive.add_argument("--version", action="store_true",help="Print current version")
args = parser.parse_args()

arguments = vars(args)

if not any(arguments.values()):
	parser.print_help()
	quit()

if args.version:
	banner.banner()
	quit()


if args.list_email_schemes:
	for scheme,example in naming_scheme.email_schemes.items():
		print('%s:%s' % (scheme, logger.BLUE(example)))
	quit()

# The most important part...
banner.banner()

if args.verbose:
	logger.verbose_switch = True
	logger.debug_switch = False

if args.debug:
	logger.debug_switch = True	
	logger.verbose_switch =  True

if args.cookie == None:
	logger.red('Please specify a file containing the %s cookie.' % logger.RED('li_at'))
	quit()

try:
	with open(args.cookie,'r') as f:
		cookie=f.readline().rstrip()
except:
	logger.red('Please add the cookie to a file')
	logger.debug('%s not valid' % args.cookie)
	quit()

if args.threads:
	threads = args.threads
else:
	threads = 5

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
	email_schemes = naming_scheme.email_schemes
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

valid_emails_only = args.valid_emails_only
if valid_emails_only:
	validation = 'o365'

data = data_structure.Data(cookie,company_id,email_format,domain,filename,keyword,validation,api_key,valid_emails_only,threads)

logger.debug(str(vars(data)))

for k,v in vars(data).items():
	if v != None:
		logger.yellow('%s set to %s' % (k,logger.YELLOW(v)))
	else:
		logger.debug('%s set to None' % k)

print()

try:
	logger.debug('Running core.run()')
	users=core.run(data)
except KeyboardInterrupt:
	logger.yellow('Keyboard interrupt detected!')
	quit()

logger.green('Done!')

finish_time = datetime.datetime.now().replace(microsecond=0)

duration = finish_time-start_time

logger.blue('Runtime: %s' % logger.BLUE(duration))
