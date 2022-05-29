# RESTful API for posting and reading messages
This is a RESTful API that can receive, store (in memory) and provide messages to users, similar to pastebin. The messages will be removed after 7 days.

The program is written in Python using the Flask framework. You need Python version > 3 and Flask.

# Install
To install the required modules use pip using the requirements.txt (TODO) file provided in the repository.

# Run
To run the program, use the Makefile (command: make run)

## Mac / Linux
TODO

## Windows
TODO

# API calls

The API only has two possible calls.

## POST /send --data="text=<TEXT>"
Create a message with a text provided in a post request.
The API service will respond with a JSON object containing the message_id of the newly created message or Null if no message was created and a success parameter which is either 1 (True) or 0 (False) depending on if the message was created or not.

### Example

Request:
```
curl "http://127.0.0.1:5000/send" --data "text=hellothere
```
Response:
```json
{"message":"hellothere","message_id":"tfltf3y5g1","time_posted":1653774375.88495}

```

## GET /read/:message_id
Read the content of a message with message_id provided. Returns a JSON object containing the message_id, text and time_posted of the message as well as a success parameter which is either 1 or 0. If success is 0 all other fields will be Null.

### Example
Request 
```
curl "http://127.0.0.1:5000/read/tfltf3y5g1"
```
Response:
```json
{"message":"hellothere","message_id":"tfltf3y5g1","time_posted":1653774375.88495}
```

# Design choices

## Random ID
The random ID is 10 characters long, and an alphabet of at least 32 characters is recommended. This would yield 32^10 possible combinations which is considered enough to never expect a collision.

## Removal of old messages
After 7 days a message should be removed.
My first idea was to just remove the message using a timer that checks all messages every new day and compare their creation date with todays date. 

Another idea was to have an individual timer for each message, but this would probably be too memory intense. 

My final idea was to just remove the messages that someone is requesting to read and which has already been active for 7 days. 
This has a drawback, the server will still contain the messages after days. But it will be faster (only checks a message time on request), and it will never be possible to open a message which is more than 7 days old.

The mesage might still remain in memory on the host machine, which is a potential security risk. If physical memory security is a factor this application should not be used.

## Encryption (IMPORTANT!!!)
There is currently NO encryption of either messages or requests or responses send to and from the API service. Please do not use this application as is if messages have to be kept secret from eavesdroppers and intruders, or if messages have to be e2 encrypted.
However, you could of course encrypt your messages locally using e.g. PGP/GPG. 

## Dependencies
Dependencies are always a risk. Always make sure to keep all dependencies and Python updated to latest possible version.

# License
The program is released under GPLv2, which means that anyone can use, manipulate and read the source code without asking for permission or attributing me. However, you have to release any modified version of the program under GPLv2 as well.
