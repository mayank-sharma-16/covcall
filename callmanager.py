# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import os

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Make API calls here...

def send_message(number, text):
    message = client.messages \
        .create(
             body=text,
             messaging_service_sid='MG6a8cbff2990e52e3b5699115738f7b91',
             to=number
         )

def generate_call_message(text):
    f = open("static/covcall.xml", "wb")
    top = Element('Response')
    child = SubElement(top, 'Say', {'voice': 'alice'})
    child.text = text
    print(tostring(top))
    f.write(tostring(top))

def make_call(number):
    call = client.calls.create(
                        url='http://0c962c1f.ngrok.io/static/covcall.xml',
                        to=number,
                        from_='+14073293385'
                    )
