from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect, session
import twilio.twiml
import WitAIManager as wit

app = Flask(__name__)
app.secret_key = open('secret_key.txt').read().strip()
account_sid = open('twilio_sid.txt').read().strip()
auth_token = open('twilio_token.txt').read().strip()

# Find these values at https://twilio.com/user/account
client = TwilioRestClient(account_sid, auth_token)
twilio_number = "+17062252499"

def send_sms(num, message):
	client.messages.create(to=num, from_=twilio_number, body=message);

def send_to_wit(context, message):
	resp = wit.twilio_input(context, message)
	return resp

@app.route("/", methods=['GET', 'POST'])
def responder():
	message = request.values.get('Body', None)
	phone_number = request.values.get('From', None)

	#get context from session if exists
	#if it doesn't exist, return context with just phone number
	context = session.get('context', {'user': phone_number})

	#send wit the context and message from the user
	response = send_to_wit(context, message)

	#response is disctionary with 2 elements
	response_to_user = response['resp']
	new_context = response['context']

	#assign twilio context to be new context from wit
	session['context'] = new_context

	resp = twilio.twiml.Response()
	resp.message(response_to_user)
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)