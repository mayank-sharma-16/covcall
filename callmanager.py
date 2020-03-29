# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import twitter_gov_script as tgs
import time
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

def mass_call():
    '''text is a string. state is a string.'''
    tgs.refresh_tweets()

    for row in tgs.get_call_list():
        generate_call_message(row[2])
        make_call(row[0])
        time.sleep(2)

    '''Mayank this is what you need to edit.
    mass_call(text) is the function that calls all the numbers in the database from
    the inputted state and reads the text aloud to them. generate_call_message(text) will set up
    an xml file on the backend with the text that you input (you don't need understand this).
    The make_call(number) function will call the number and read the text aloud to them. All you
    need to do below this comment is add a for loop that iterates through the database,
    finds everyone belonging to the state, and then calls them using make_call(number).
    Then, you need can call mass_call whenever you want from your own scripts.
    '''



def generate_call_message(text):
    '''text is a string.'''
    f = open("static/covcall.xml", "wb")
    top = Element('Response')
    child = SubElement(top, 'Say', {'voice': 'alice'})
    child.text = text
    print(tostring(top))
    f.write(tostring(top))

def make_call(number):
    '''number is a string. See the from_ parameter below for an example of the format.'''
    call = client.calls.create(
                        url='http://0c962c1f.ngrok.io/static/covcall.xml',
                        to=number,
                        from_='+14073293385'
                    )
