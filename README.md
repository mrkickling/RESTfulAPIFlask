# RESTful API for posting and reading messages
This is a RESTful API that can receive, store (in memory) and provide messages to users, similar to pastebin. The messages will be removed after 7 days.

The program is written in Python using the Flask framework. You need Python 3 and Flask.

# Install

## Using pip
Make sure that you have Python 3 and pip installed.
To install the required modules use pip using the requirements.txt file provided in the repository by running:

```bash
pip install -r requirements.txt
```
or
```bash
python -m pip install -r requirements.txt
```
On some systems with duplicate python versions the binaries are called pip3 and python3 instead.

## Using docker
Make sure you have docker installed and that you are in this directory.
```bash
docker image build -t flask_api_docker .
docker run -p 5000:5000 -d flask_docker
```
# Run
To run the program, use the bash file (run.sh, has to be made executable) or simply use the commands:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
I have not been able to verify this process on Windows, but I suspect WSL would do the trick if nothing else works.

## In production
This service should not be run in production as is. To run in production use a [WSGI (Web Server Gateway Interface)](https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/) implementation like [Gunicorn](https://gunicorn.org/) or [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/). 

# API calls
The API only has two possible calls:

## POST /write --data="text=<TEXT>"
Create a message with a text provided in a post request.
The API service will respond with a JSON object containing the message_id of the newly created message or Null if no message was created and a success parameter which is either 1 (True) or 0 (False) depending on if the message was created or not.

### Example

Request (using curl):
```
curl "http://127.0.0.1:5000/write" --data "text=hellothere"
```
Response (200):
```json
{"message":"hellothere","message_id":"cfybrtvsfujo","success":1,"url":"127.0.0.1:5000/read/cfybrtvsfujo"}

```
If the text is too long you will get the response (413):
```json
{"error_message":"Message is too long","success":0}
```

## GET /read/:message_id
Read the content of a message with message_id provided. Returns a JSON object containing the message_id, text and time_posted of the message as well as a success parameter which is either 1 or 0. If success is 0 all other fields will be Null.

### Example
Request 
```
curl "http://127.0.0.1:5000/read/cfybrtvsfujo"
```
Response (200):
```json
{"message":"hellothere","message_id":"cfybrtvsfujo","success":1,"url":"127.0.0.1:5000/read/cfybrtvsfujo"}
```
If the requested message is over 7 days old or does not exist you will get the response (404):
```json
{"error_message":"Message does not exist","success":0}
```

# Design choices

## JSON
Is readable by humans and practically all programming languages have libraries to parse it. 

## Random ID
The random ID is 12 characters long, and an alphabet of 26 characters is used per default. This would yield 26^12 ( = 9.5 x 10^16 ) possible combinations which should avoid any collisions.

## Removing old messages
After 7 days a message will be removed.
I run a function every 10 seconds on its own thread (apihandler.py, line 17) This function checks the messages by walking through a deque, starting with the oldest message. It will remove messages if they are over 7 days old, and stop walking through the deque when it finds a newer message. This was the best solution that I came up with since a requirement was to remove the messages automatically within 7 days. Other ideas was to only remove messages on api calls, but this was not sufficient according to the requirements.

NOTE: The messages might remain hidden in unused memory until they are overwritten. This could be a problem in some applications. 

## Encryption
There is currently NO encryption of either messages or requests or responses send to and from the API service. Please do not use this application as is if messages have to be kept secret from eavesdroppers and intruders, or if messages have to be e2 encrypted.
However, you could of course encrypt your messages locally using e.g. PGP/GPG. 

## Code injection
If you are displaying the results make sure to sanitize the output that you get from the API. There is no string sanitization being done in the service.

## DoS attacks
Dos attacks are always a risk when connecting a service to the internet. Overflooding of big messages is a potential risk. IP-blocking could be one solution to decrease the risk for this.

## Dependencies
Dependencies are always a risk, since they all might have vulneratbilities in them. Always make sure to keep all dependencies and Python up to date.

# Unit test
Tests are provided in tests/test_api.py and are hopefully self explanatory. They can be run just like any python program.

# License
The program is released under GPLv2, which means that anyone can use, manipulate and read the source code without asking for permission or attributing me. However, you have to release any modified version of the program under GPLv2 as well.
