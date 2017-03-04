from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)
sid = open('sid.txt').read()
token = open('token.txt').read()

# Find these values at https://twilio.com/user/account
account_sid = sid
auth_token = token
client = TwilioRestClient(account_sid, auth_token)
twilio_number = "+17062252499"

def send_sms(num, message):
	client.messages.create(to=num, from_=twilio_number, body=message);

def send_to_wit(message):
	#send message to wit for processing
	#fill this in after wit skeleton code is completed
	#for now return generic message
	return "processed message"

@app.route("/", methods=['GET', 'POST'])
def responder():
	message = request.values.get('Body', None)
	response = send_to_wit(message)
	resp = twilio.twiml.Response()
	resp.message(response)
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)