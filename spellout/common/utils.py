import os
import jwt
import requests
import datetime
from flask_mail import Message, Mail

from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat

# Environmental Variables
# key = os.environ.get('JWT_KEY')
# translator_key = os.environ.get('TRANSLATOR_SUBSCRIPTION')
# tts_key = os.environ.get('TTS_SUBSCRIPTION')
# region = os.environ.get('AZURE_REGION')

key = 'ananth1404'
translator_key = '26bc6f82114b4382ba1aacf109c4cb54'
tts_key = 'fd3d3ade72af4f18a773a999739a11a9'
region = 'centralindia'

mail = Mail()

def encoding(client_id, email):    
    now = datetime.datetime.now()
    header = {
        'alg': 'HS256',
        'typ': 'JWT'
    }
    payload = {
        'client_id': client_id,
        'email': email,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    encoded = jwt.encode(payload=payload, key='ananth1404', algorithm='HS256', headers=header)
    return encoded.decode('utf-8')

def send_mail(to, subject, body):
    msg = Message(
        recipients = to,
        subject = subject,
        body = body
    )
    mail.send(message=msg)


def translator(text, lang):
    endpoint = 'https://api.cognitive.microsofttranslator.com/'
    path = 'translate?api-version=3.0'
    params = '&to={}'.format(lang)
    constructed_url = endpoint + path + params
    headers = {
        'Ocp-Apim-Subscription-Key': translator_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json'
    }
    body = [{
        'text': text
    }]  
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

def tts(language, text):
    speech_config = SpeechConfig(subscription=tts_key, region=region)
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    ssml_string = open("spellout/common/language.xml", "r").read()
    ssml_string = ssml_string.format(lang = language, text = text)
    result = synthesizer.speak_ssml_async(ssml_string).get()
    result = result.audio_data
    return result