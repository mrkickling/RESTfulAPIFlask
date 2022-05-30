""" 
A class for methods related to the API calls and storage of messages
Written by Joakim Loxdal 2022
"""

from collections import deque
from app.utils import random_string, error_message
from app.message import Message

MESSAGE_MAX_NUM_CHARS = 10 * 1024

class ApiHandler:
	def __init__(self):
		self.messages = {}
		self.time_sorted_message_ids = deque()

	def save_message(self, message):
		self.messages[message.id] = message
		self.time_sorted_message_ids.append(message.id) # newest id added last

	def write_message(self, text, host):
		if len(text) > MESSAGE_MAX_NUM_CHARS:
			return error_message("Message is too long")
		message_id = random_string(12)
		message = Message(message_id, text, host)
		self.save_message(message)
		return message.to_dict()

	def read_message(self, message_id):
		if message_id in self.messages:
			message = self.messages[message_id]
			if message.valid_time():
				return message.to_dict()
			else:
				self.remove_old_messages()
		return error_message("Message does not exist")

	def remove_old_messages(self):
		while len(self.messages):
			oldest_message_id = self.time_sorted_message_ids[0]
			oldest_message = self.messages[oldest_message_id]
			if not oldest_message.valid_time(): 
				# Oldest message is too old, remove it
				self.time_sorted_message_ids.popleft()
				del self.messages[oldest_message_id]
			else:
				# Oldest message is not old
				break 