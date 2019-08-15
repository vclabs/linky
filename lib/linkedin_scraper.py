#!/usr/bin/python3
from lib import http, logger, naming_scheme, user_structure, o365_validation, hunter_validation
import json

def company_profile(cookie,company_id,keyword):
	# This function requests the companies profile and returns the data
	if keyword == None:
		url='https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=0' % company_id
		logger.debug('Requesting %s from company_profile()' % url)
	else:
		url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&keywords=%s&origin=OTHER&q=guided&start=0" % (company_id,keyword)
		logger.debug('Requesting %s from company_profile()' % url)
	data=http.connect(url,cookie)
	if data == None:
		logger.red('Unable to authenticate to LinkedIn')
		quit()
	return data.text

def get_users(data,pages,total_employees):
	#Grab the user data per page
	cookie = data.cookie
	company_id = data.company_id
	email_format =  data.email_format
	keyword = data.keyword
	domain = data.domain
	validation = data.validation
	api_key = data.api_key
	# Every page returns a dictionary of data, each dictionary is added to this list.
	people_on_this_page=0

	logger.debug(str(vars(data)))

	userdata_per_page = []

	for page in range(0,pages+1):

		if page+1 == 25:
			logger.debug('Breaking, pages exceed 25')
			break

		if total_employees < 40:
			logger.debug('Locking users per page to match total_employees')
			# This method pulls 40 total_employees per page. If the available total_employees is less then 40
			# Set total_employees_per_age to whatever the number is
			total_employees_per_page = total_employees
			total_employees_to_fetch = total_employees
		else:
			logger.debug('Locking users per page to 40')
			# However, if the amount of available total_employees is higher than the per page limit, set the per page limit to the max (40)
			total_employees_per_page = 40

		# Every time this is hit, the start point in the api is incremented. First, it gets 0 - 40, then 40 - 80 and so on.
		# This can be dynamically figured out by multiplying the page number (1) by the total_employees_per_page (40).
		total_employees_to_fetch = total_employees_per_page * page

		# In order to stop this loop from requesting more than is available, and then breaking it, this if statement limits that:
		if total_employees_to_fetch >= total_employees:
			break

		url="https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=%s" % (company_id,total_employees_to_fetch)
		logger.debug('Requesting %s from get_users()' % url)
		logger.blue('Pulling from page %s' % logger.BLUE(page+1))
			
		api_response=http.connect(url,cookie)
		result = api_response.text.encode('UTF-8')

		try:
			result = json.loads(result) #contains data for ~40 people
		except Exception as e:
			print(e)
			quit()

		people_on_this_page=people_on_this_page+len(result['elements'][0]['elements'])
		if people_on_this_page > 0:
			logger.green('Successfully pulled %s users' % logger.GREEN(str(people_on_this_page)))
		userdata_per_page.append(result)

	# This part could do with threading
	users = parse_users(data,userdata_per_page)
	logger.debug('Sending list of json objects to parse_users()')
	return users

def parse_users(data,userdata_per_page):
	cookie = data.cookie
	company_id = data.company_id
	email_format =  data.email_format
	keyword = data.keyword
	domain = data.domain
	validation = data.validation
	api_key = data.api_key	

	logger.debug(str(vars(data)))

	# For every page, do some parsing.

	if domain.startswith('@'):
		domain=domain
	else:
		domain='@'+domain

	users = []

	for user_data in userdata_per_page:
		for d in user_data['elements'][0]['elements']: #This goes one user at a time
			if 'com.linkedin.voyager.search.SearchProfile' in d['hitInfo'] and d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['headless'] == False:
				try:
					industry = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['industry']
					logger.debug(industry)
				except:
					industry = ""    

				raw_firstname = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['firstName']
				raw_surname = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['lastName']
				
				profile_url = "https://www.linkedin.com/in/%s" % d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['publicIdentifier']
				occupation = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['occupation']
				location = d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['location']
				try:
					role_data=d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['snippets'][0]['heading']['text']
					try:
						current_role=role_data.split(' at ')[0]
						current_company=role_data.split(' at ')[1]
					except:
						current_company=None
						current_role=occupation					
				except:
					try:
						current_company=occupation.split(' at ')[1]
						current_role=occupation.split(' at ')[0]
					except:
						current_company=None
						current_role=occupation

				name_data=[raw_firstname,raw_surname]

				logger.debug(str(name_data))

				name_scheme=naming_scheme.names(name_data)
				firstname=name_scheme[0]
				middlename=name_scheme[1]
				surname=name_scheme[2]
				fullname=name_scheme[3]
				name_data=[firstname,middlename,surname]
				email_scheme=naming_scheme.emails(name_data,email_format,domain)

				email = email_scheme

				try:
					datapoint_1=d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['rootUrl']
					datapoint_2=d['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['artifacts'][2]['fileIdentifyingUrlPathSegment']
					picture=datapoint_1+datapoint_2
					logger.debug(picture)
				except:
					picture = None

				if validation != None:
					if validation == 'o365':
						validated=o365_validation.validate(email)
					elif validation == 'hunter':
						validated=hunter_validation.validate(email,api_key)
						if validated == 429:
							logger.red('You have exceeded your hunter API Requests.')
							quit()
						elif validated == 401:
							logger.red('The API Key specified recieved an %s error.' % 'authentication')
							quit()
				else:
					validated = False

				user=user_structure.User(profile_url,picture,firstname,middlename,surname,fullname,email,validated,current_role,current_company)
				users.append(user)

	return users
