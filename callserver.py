from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls and mention the caller's city"""
    '''# Get the caller's city from Twilio's request to our app
    city = request.values['FromCity']'''
    state = request.values['FromState'] # Get caller's state

    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say('Never gonna give you up, {}!'.format(state), voice='alice')

    # Play an audio file for the caller
    #resp.play('https://demo.twilio.com/docs/classic.mp3')
    print(state+"\n")
    print(str(resp))
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
