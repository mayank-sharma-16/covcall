from flask import Flask, request, send_file
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)


@app.route("/voice", methods=['POST'])
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

    # Read intro message aloud to the caller
    if not intro:
        resp.play('speeches/introspeech.mp3')

    # Start our <Gather> verb
    gather = Gather(num_digits=1)
    gather.play('speeches/gatherspeech.mp3')
    resp.append(gather)

    # If the user doesn't select an option, redirect them into a loop
    resp.redirect('/voice')

    return str(resp) # Dummy return statement

@app.route("/speeches/<path:text>", methods=['GET'])
def serve_redospeech(text):
    return send_file("speeches/" + text, mimetype='audio/mpeg', as_attachment=True)

def addNumber(number, state):
    return

def removeNumber(number, state):
    return

if __name__ == "__main__":
    app.run(debug=True)
