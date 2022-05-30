""" 
A file for utilities used in the message API
Written by Joakim Loxdal 2022
"""

import random
import string

def random_string(n, alphabet=string.ascii_lowercase):
	"""
		random string will return a random string of length 'n',
		using characters from the string 'alphabet'.
	"""
	string = ""
	for i in range(n):
		string += random.choice(alphabet)
	return string

def error_message(text):
	return {
		"success": 0,
		"error_message": text
	}