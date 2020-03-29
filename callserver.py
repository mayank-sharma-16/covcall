from flask import Flask, request, send_from_directory
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)


@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls and mention the caller's city"""
    intro = False
    number = request.values['From'] # Get caller's number
    state = request.values['FromState'] # Get caller's state

    # Start our TwiML response
    resp = VoiceResponse()

    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            resp.play('speeches/joinspeech.mp3')
            addNumber(number, state)
            return str(resp)
        elif choice == '2':
            resp.play('speeches/leavespeech.mp3')
            removeNumber(number, state)
            return str(resp)
        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            intro = True
            resp.play('speeches/redospeech.mp3')

    # Read a message aloud to the caller
    if not intro:
        resp.play('speeches/introspeech.mp3')
    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.play('speeches/gatherspeech.mp3')
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')

    # Play an audio file for the caller
    #resp.play('https://demo.twilio.com/docs/classic.mp3')
    return str(resp) # Dummy return statement

'''@app.route('/speeches/')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'speeches'), filename)'''

def addNumber(number, state):
    return

def removeNumber(number, state):
    return

if __name__ == "__main__":
    app.run(debug=True)
