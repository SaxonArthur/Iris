from flask import Flask, render_template, request, jsonify, redirect
from dotenv import load_dotenv
from tts import tts

load_dotenv() #Loads environment variables

message_log={}

app=Flask(__name__) #Initialize flask

#Home page
@app.route('/')
def index():
    return render_template('button.html')

#Recieve location data
@app.route('/locate', methods=['POST'])
def locate():
    global lat, long, city
    location = request.form.get('location')  # Get the location from the form data
    # Process the location as needed...
    lat, long, city=location.split(',')
    return jsonify({"text": f"Received location: {location}"})
    
#Recieve audio data, save as a file locally
@app.route('/upload', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']  # This is a FileStorage object
    audio_file.save('recording.mp3')
    return jsonify({'message':'data successfly uploaded'})

#Process audio and procude output
@app.route('/response', methods=['GET'])
def show_audio():
    global message_log
    question,response = tts('recording.mp3', lat, long, city,message_log)
    try:
        message_log.update({question:response})
    except:
        message_log={}
        message_log.update({question:response})
    print(message_log)
    return render_template('response.html',
                           response=response,
                           question=question
    )

#Refreshes message log
@app.route('/refresh', methods=['POST'])
def refresh_log():
    global message_log
    if message_log:
        message_log={}
        return jsonify({'message':'message log refreshed succesfully: '+str(message_log)})
    else:
        return jsonify({'error':'message log is empty'})


#Run program
if __name__ == "__main__":
    app.run(debug=True)