# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import Client
import os

from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Make API calls here...

message = client.messages \
    .create(
         body="Even lemons can at least power a clock",
         messaging_service_sid='MG6a8cbff2990e52e3b5699115738f7b91',
         to='+19256405980'
     )

print(message.sid)
