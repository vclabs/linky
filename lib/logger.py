from time import gmtime, strftime
from lib import html
import pandas as pd
import csv, json
import os

colour_red = "\033[1;31m"
colour_blue = "\033[1;34m"
colour_green = "\033[1;32m"
colour_yellow = "\033[1;33m"
colour_remove= "\033[0m"
cur_dir=os.path.dirname(os.path.abspath(__file__))
verbose_switch = False

def RED(string):
	string=str(string)
	return (colour_red + string + colour_remove)

def BLUE(string):
	string=str(string)
	return (colour_blue + string + colour_remove)

def GREEN(string):
	string=str(string)
	return (colour_green + string + colour_remove)

def YELLOW(string):
	string=str(string)
	return (colour_yellow + string + colour_remove)

def verbose(string):
	if verbose_switch == True:
		log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
		print('['+log_time+']'+YELLOW(' >> ' )+string)

def blue(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+BLUE(' >> ' )+string)

def green(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+GREEN(' >> ' )+string)

def red(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+RED(' >> ' )+string)

def yellow(string):
	log_time=strftime("%d/%m/%y, %H:%M:%S", gmtime())
	print('['+log_time+']'+YELLOW(' >> ' )+string)

def write_out(users,data,job_role_count,filename):
	if filename == None:
		return
	write_html(users,data,job_role_count,filename)
	write_csv(users,data,job_role_count,filename)
	write_json(users,filename)

def write_csv(users,data,job_role_count,filename):
	validation = data.validation
	filename=filename+'.csv'
	if validation != None:
		headers=['picture','fullname','firstname','middlename','surname','email','validated','current role','current company']
	else:
		headers=['picture','fullname','firstname','middlename','surname','email','current role','current company']

	with open(filename,'w') as f:
		writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(headers)
		for user in users:
			profile_url=user.profile_url
			fullname=user.fullname
			firstname=user.firstname
			middlename=user.middlename
			surname=user.surname
			email=user.email
			current_role=user.current_role
			current_company=user.current_company
			if validation != None:
				validated=user.validated
				writer.writerow([profile_url,fullname,firstname,middlename,surname,email,validated,current_role,current_company])
			else:
				writer.writerow([profile_url,fullname,firstname,middlename,surname,email,current_role,current_company])

def write_json(users,filename):
	user_json = json.dumps([ob.__dict__ for ob in users])
	user_json = json.loads(user_json)

	filename=filename+'.json'
	with open(filename,'w') as f:
		json.dump(user_json,f)

def write_html(users,data,job_role_count,filename):
	domain = data.domain
	validation = data.validation
	user_counter=0
	for user in users:
		user_counter+=1
	filename=filename+'.html'
	with open(filename,'w') as f:
		title='Linky: % s' % domain
		f.write(html.header(title))
		if validation != None:
			headers=['picture','fullname','firstname','middlename','surname','email','email validation','current role','current company']
		else:
			headers=['picture','fullname','firstname','middlename','surname','email','current role','current company']
		f.write(html.h3_span(['User Count',user_counter]))
		f.write(html.p('Click the users image to view their LinkedIn!'))
		f.write(html.input_box())
		f.write(html.table_head(headers))
		for user in users:
			fullname=user.fullname
			profile_url=user.profile_url
			picture=user.picture
			if picture == None:
				picture=False
			firstname=user.firstname
			middlename=user.middlename
			surname=user.surname
			email=user.email
			current_role=user.current_role
			current_company=user.current_company
			f.write('<tr>\n')
			f.write(html.table_picture(profile_url,picture))
			f.write(html.table_entry(fullname))
			f.write(html.table_entry(firstname))
			f.write(html.table_entry(middlename))
			f.write(html.table_entry(surname))
			f.write(html.table_entry(email))
			if validation != None:
				validated=user.validated
				if validated == None:
					f.write(html.table_entry('Unable to validate'))
				else:
					if validated == True:
						try:
							f.write(html.table_entry('Got creds: %s') % validated[1])
						except:
							f.write(html.table_entry(str(validated)))
					else:
						f.write(html.table_entry(str(validated)))

			f.write(html.table_entry(current_role))
			f.write(html.table_entry(current_company))
			f.write('</tr>\n')
		f.write('</tbody>\n')
		f.write('</table>\n')
		f.write(html.h3('Top roles'))
		f.write(html.p('The following table shows the most common roles within the designated organisation.\nRunning this tool again with these top 3 results as keywords will result in more specific data as the api data extraction only pulls 1000 results.'))
		f.write(html.table_head(['Role','Count']))
		for role,count in job_role_count.items():
			f.write('<tr>\n')
			f.write(html.table_entry(role))
			f.write(html.table_entry(count))
			f.write('</tr>\n')
		f.write('</tbody>\n')
		f.write('</table>\n')
		f.write(html.footer())

def dump(users,validation):
	for user in users:
		profile_url=user.profile_url
		picture=user.picture
		firstname=user.firstname
		middlename=user.middlename
		surname=user.surname
		fullname=user.fullname
		email=user.email
		validated=user.validated
		current_role=user.current_role
		current_company=user.current_company
		if validation == None:
			green('%s (%s): %s at %s' % (GREEN(fullname),email,current_role,GREEN(current_company)))
		else:
			try:
				valid = validated[0]
				password = validated[1]
				green('[%s:%s] %s (%s): %s at %s' % (GREEN('PWNED!'),GREEN(password),GREEN(fullname),email,current_role,GREEN(current_company)))
			except:
				if validated == True:
					green('%s (%s: [%s]): %s at %s' % (GREEN(fullname),email,GREEN(str(validated)),current_role,GREEN(current_company)))
				elif validated == False:
					green('%s (%s: [%s]): %s at %s' % (GREEN(fullname),email,RED(str(validated)),current_role,GREEN(current_company)))
				elif validated == None:
					green('%s (%s: [%s]): %s at %s' % (GREEN(fullname),email,RED(str(validated)),current_role,GREEN(current_company)))



