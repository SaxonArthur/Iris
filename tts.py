import whisper
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests
import subprocess

#Loads environment variables
load_dotenv()

def tts(file, lat, long, city,message_log):
  #Define application shortcuts
  applications={
    'spotify':os.getenv('spotify'),
    'microsoft teams':os.getenv('microsoftword'),
    'onenote':os.getenv('onenote'),
    'powerpoint':os.getenv('powerpoint'),
    'microsoft word':os.getenv('microsoftword'),
    'chrome':os.getenv('chrome'),
    'excel':os.getenv('excel')
}


  model=whisper.load_model('tiny')
  result = model.transcribe(file) #Transcribe audio file
  genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
  model = genai.GenerativeModel("gemini-1.5-flash-exp-0827")
  history=[]
  #Create context for chatbot from message log
  for i in message_log:
      history.append({'role':'user', 'parts':i})
      history.append({'role':'model','parts':message_log[i]})
  chat=model.start_chat(
    history=history
  )

  for i in applications:
    if i in result['text'].lower():
        subprocess.call(applications[i],shell=True)
        response=i+' successfully opened'
        os.remove(file)
        return result['text'], response

  #Checking if audio file was empty
  if result['text']=='':
    response='I could not process your question, please try again'
    os.remove(file)
    return result['text'],  response

  #Checking if user said weather
  elif 'weather' in result['text'] or 'Weather' in result['text']:
    weather_data=requests.get(
      'https://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+long+'&appid='+os.getenv('WEATHER_KEY')+'&units=metric')
    weather_data=weather_data.json()
    #Accessing json data
    temp=str(weather_data["main"]["temp"])
    minTemp=str(weather_data["main"]["temp_min"])
    maxTemp=str(weather_data["main"]["temp_max"])
    feelsLike=str(weather_data["main"]["feels_like"])
    description=weather_data["weather"][0]["main"]+' and '+weather_data["weather"][0]["description"]
    response=chat.send_message(
      'give a summary of the weather in '+city+' given the following info: temp: '+temp+', minimum: '+minTemp+', maxTemp: '+maxTemp
      +', feels like: '+feelsLike+', description: '+description
      )

  else:
    response = chat.send_message('Answer this question: '+result['text'])
  response=response.text.replace('*','') #Necessary as gemini returns many asterisks in response
  os.remove(file)
  return result['text'], response

