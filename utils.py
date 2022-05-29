import random

"""
	random string will return a random string of length 'n',
	using characters from the string 'alphabet'.
"""
def random_string(n, alphabet="abcdefghijklmnopqrstuvwxyz1234567890"):
	string = ""
	for i in range(n):
		string += random.choice(alphabet)
	return string
