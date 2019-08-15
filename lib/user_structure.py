#!/usr/bin/python3

class User:
	def __init__(self,profile_url,picture,firstname,middlename,surname,fullname,email,validated,current_role,current_company):
		self.profile_url = profile_url
		self.picture = picture
		self.firstname = firstname
		self.middlename = middlename
		self.surname = surname
		self.fullname = fullname
		self.email = email
		self.validated = validated
		self.current_role = current_role
		self.current_company = current_company