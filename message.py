import time

TIME_LIMIT_DAYS = 7

class Message:
	def __init__(self, message_id, text):
		self.id = message_id
		self.text = text
		self.time_posted = time.time()

	def to_dict(self):
		return {
			"message": self.text, 
			"message_id": self.id,
			"time_posted": self.time_posted
		}

	def valid_time(self):
		curr_t = time.time()
		# If time since posted is less than TIME_LIMIT_DAYS, return true.
		return (curr_t - self.time_posted) < (TIME_LIMIT_DAYS * 24 * 60 * 60)
