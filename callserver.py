from flask import Flask, request, send_file
from twilio.twiml.voice_response import VoiceResponse, Gather
from callmanager import send_message

app = Flask(__name__)


@app.route("/<path:text>", methods=['POST'])
def voice(text):
    if "static" in text:
        return send_file(text, mimetype='text/xml', as_attachment=True)
    else:
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
                resp.play('static/joinspeech.mp3')
                addNumber(number, state)
                return str(resp)
            elif choice == '2':
                resp.play('static/leavespeech.mp3')
                removeNumber(number, state)
                return str(resp)
            elif choice == '3':
                resp.play('static/moreinfospeech.mp3')
                send_message(number, "For more information, please visit our website at COVcall.tech")
                return str(resp)
            else:
                # If the caller didn't choose 1 or 2, apologize and ask them again
                intro = True
                resp.play('static/redospeech.mp3')

        # Read intro message aloud to the caller
        if not intro:
            resp.play('static/introspeech.mp3')

        # Start our <Gather> verb
        gather = Gather(num_digits=1)
        gather.play('static/newgatherspeech.mp3')
        resp.append(gather)

        # If the user doesn't select an option, redirect them into a loop
        resp.redirect('/voice')

        return str(resp) # Dummy return statement

@app.route("/static/<path:text>", methods=['GET'])
def serve_redospeech(text):
        return send_file("static/" + text, mimetype='audio/mpeg', as_attachment=True)

def addNumber(number, state):
    return

def removeNumber(number, state):
    return

if __name__ == "__main__":
    app.run(debug=True)
