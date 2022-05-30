from app import app
from flask import request, jsonify
from app.apihandler import ApiHandler

api_handler = ApiHandler()

@app.route("/write", methods=["POST"])
def send_message():
	"""
	  The API call for sending new messages to store in memory.
	  Returns the new message in JSON format.
	  See docs for more detailed information.
	"""
	text = request.form.get('text')
	message = api_handler.write_message(text, request.host)
	response = jsonify(message)
	if message["success"] == 0:
		response.status = 413
	return response

@app.route("/read/<message_id>")
def read_message(message_id):
	"""
		The API call for reading messages by giving the ID of the message
		as a GET parameter (id). Returns the requested message in JSON format.
		See docs for more detailed information.
	"""
	message = api_handler.read_message(message_id)
	response = jsonify(message)
	if message["success"] == 0:
		response.status = 404
	return response