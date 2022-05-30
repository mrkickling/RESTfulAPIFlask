""" 
A class for messages in the message API
Written by Joakim Loxdal 2022
"""
import time

TIME_LIMIT_DAYS = 7

class Message:
	def __init__(self, message_id, text, host, time_posted=time.time()):
		self.id = message_id
		self.time_posted = time_posted
		self.url = host + "/read/" + self.id
		self.text = text

	def to_dict(self):
		# Decides which data should be given to users
		return {
			"message_id": self.id,
			"message": self.text, 
			"url": self.url,
			"success" : 1
		}

	def valid_time(self):
		curr_t = time.time()
		# If time since posted is less than TIME_LIMIT_DAYS, time is valid
		return (curr_t - self.time_posted) < (TIME_LIMIT_DAYS * 24 * 60 * 60)
