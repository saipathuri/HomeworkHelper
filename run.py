from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)
account_sid = open('twilio_sid.txt').read().strip()
auth_token = open('twilio_token.txt').read().strip()

# Find these values at https://twilio.com/user/account
client = TwilioRestClient(account_sid, auth_token)
twilio_number = "+17062252499"

def send_sms(num, message):
	client.messages.create(to=num, from_=twilio_number, body=message);

def send_to_wit(phone_number, message):
	#send message to wit for processing
	#fill this in after wit skeleton code is completed
	#for now return generic message
	return "processed message"

@app.route("/", methods=['GET', 'POST'])
def responder():
	message = request.values.get('Body', None)
	phone_number = request.values.get('From', None)
	response = send_to_wit(phone_number, message)
	resp = twilio.twiml.Response()
	resp.message(response)
	return str(resp)

if __name__ == "__main__":
	app.run(debug=True)