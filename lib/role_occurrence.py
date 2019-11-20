# -*- coding: utf-8 -*-

from collections import Counter

def count(users,total_employees):

	counts = {}
	role_data = {}
	for user in users:
		current_role=user.current_role
		if current_role in counts:
			counts[current_role] += 1
		else:
			counts[current_role] = 1

	coll_obj = Counter(counts)


	if total_employees <= 10:
		amount = total_employees
	elif total_employees <= 100:
		amount = 10
	elif total_employees in range(100,1000):
		amount = 20
	else:
		amount = 10

	try:
		most_common_5 = coll_obj.most_common(amount)

		for role in most_common_5:
			role_name=role[0]
			role_count=role[1]
			role_data[role_name]=role_count
	except:
		logger.red('Couldnt identify common role types')

	return role_data
	