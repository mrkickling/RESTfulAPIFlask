from flask import Flask, jsonify, request
from message import Message
from utils import random_string
import random
import json

messages = {}
app = Flask(__name__)

"""
	The API call for sending new messages to store in memory.
	Returns the new message in JSON format.
"""
@app.route("/send", methods=["POST"])
def send_message():
	text = request.form.get('text')
	message_id = random_string(10)
	messages[message_id] = Message(message_id, text)
	return jsonify(messages[message_id].to_dict())

"""
	The API call for reading messages by giving the ID of the message
	as a GET parameter (id). Returns the requested message in JSON format.
"""
@app.route("/read")
def read_message():
	message_id = request.args["id"]
	if message_id in messages:
		message = messages[message_id]
		if message.valid_time():
			return jsonify(message.to_dict())
		else:
			messages.remove(message_id)
	return "The message does not exist"