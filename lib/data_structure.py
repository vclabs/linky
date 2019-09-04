#!/usr/bin/python3

class Data:
	def __init__(self,cookie,company_id,email_format,domain,filename,keyword,validation,api_key,valid_emails_only):
		self.cookie = cookie
		self.company_id = company_id
		self.email_format = email_format
		self.domain = domain
		self.filename = filename
		self.keyword = keyword
		self.validation = validation
		self.api_key = api_key
		self.valid_emails_only = valid_emails_only
