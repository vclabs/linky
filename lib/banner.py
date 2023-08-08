# -*- coding: utf-8 -*-

from lib import logger
import random

VERSION='0.2.8 dev'
CODENAME='UhOh365'

def random_color(string):
	colour_red = "\033[1;31m"
	colour_blue = "\033[1;34m"
	colour_green = "\033[1;32m"
	colour_remove= "\033[0m"
	r=random.randint(0,2)
	if r == 0:
		print  (colour_red+string+colour_remove)
	elif r == 1:
		print (colour_blue+string+colour_remove)
	elif r == 2:
		print (colour_green+string+colour_remove)

def banner():
	print('')
	random_color(' ▄█        ▄█  ███▄▄▄▄      ▄█   ▄█▄ ▄██   ▄   ')
	random_color('███       ███  ███▀▀▀██▄   ███ ▄███▀ ███   ██▄  Title: Linky.py')
	random_color('███       ███▌ ███   ███   ███▐██▀   ███▄▄▄███  Author: Virtual Cyber Labs')
	random_color('███       ███▌ ███   ███  ▄█████▀    ▀▀▀▀▀▀███  Descriptions: Enumerates users from LinkedIn')
	random_color('███       ███▌ ███   ███ ▀▀█████▄    ▄██   ███  Version: v%s' % VERSION)
	random_color('███       ███  ███   ███   ███▐██▄   ███   ███ ')
	random_color('███▌    ▄ ███  ███   ███   ███ ▀███▄ ███   ███ ')
	random_color('█████▄▄██ █▀    ▀█   █▀    ███   ▀█▀  ▀█████▀  ')
	random_color('▀                          ▀                   ')
	random_color('\tCodename: %s' % CODENAME)
	print('')

def random_color_end(string):
	colour_red = "\033[1;31m"
	colour_blue = "\033[1;34m"
	colour_green = "\033[1;32m"
	colour_remove= "\033[0m"
	r=random.randint(0,2)
	if r == 0:
		print  (colour_red+string+colour_remove,end='')
	elif r == 1:
		print (colour_blue+string+colour_remove,end='')
	elif r == 2:
		print (colour_green+string+colour_remove,end='')

def too_many_colors():
	x=''
	x+=' ▄█        ▄█  ███▄▄▄▄      ▄█   ▄█▄ ▄██   ▄   \n'
	x+='███       ███  ███▀▀▀██▄   ███ ▄███▀ ███   ██▄ \n'
	x+='███       ███▌ ███   ███   ███▐██▀   ███▄▄▄███ \n'
	x+='███       ███▌ ███   ███  ▄█████▀    ▀▀▀▀▀▀███ \n'
	x+='███       ███▌ ███   ███ ▀▀█████▄    ▄██   ███ \n'
	x+='███       ███  ███   ███   ███▐██▄   ███   ███ \n'
	x+='███▌    ▄ ███  ███   ███   ███ ▀███▄ ███   ███ \n'
	x+='█████▄▄██ █▀    ▀█   █▀    ███   ▀█▀  ▀█████▀  \n'
	x+='▀                          ▀                   \n'
	x+='\n'
	for i in x:
		random_color_end(i)
		
