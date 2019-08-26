from lib import logger, linkedin_scraper, role_occurrence
from time import sleep
import json

def run(data):
	cookie = data.cookie
	company_id = data.company_id
	email_format =  data.email_format
	keyword = data.keyword
	domain = data.domain
	validation = data.validation
	api_key = data.api_key
	filename = data.filename

	logger.debug(str(vars(data)))

	profiles = linkedin_scraper.company_profile(cookie,company_id,keyword)
	if profiles == None:
		logger.red('Unable to extract data from LinkedIn')
		quit()
	company_profile_json=json.loads(profiles)
	total_employees = company_profile_json['elements'][0]['total']
	per_page=40 # Each response contains 40 profiles per page.
	pages = int(total_employees / per_page) # Divide the amount of users by 40, this will give you the amount of pages
	logger.debug('Per page: %s' % per_page)
	if total_employees < per_page:
		logger.debug('Setting per_page to 1')
		pages=1
	logger.blue('Identified %s page(s)' % logger.BLUE(pages))
	logger.blue('Identified %s result(s)' % logger.BLUE(total_employees))

	if pages == 0:
		logger.red('Could not identify pages')
		quit()

	if total_employees > 1000:
		logger.red('This method of enumeration can only extract 1000 users')
		sleep(3)

	users=linkedin_scraper.get_users(data,pages,total_employees,keyword)
	job_role_count=role_occurrence.count(users,total_employees)

	logger.dump(users,validation)

	logger.write_out(users,data,job_role_count,filename)

	return users