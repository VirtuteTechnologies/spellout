import jwt
import threading
from flask import make_response, Response
from flask_restful import Resource, abort, fields, marshal_with, reqparse
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat


# Environmental Variables


# users-defined modules
from spellout.common.utils import tts, translator
from spellout.common.models import UsersData, HistoryData, server

class ListLanguages(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='Authorization', location='headers', required=True, trim=True, type=str)
        args = parser.parse_args(strict=True)
        try:
            decoded = jwt.decode(jwt=args.get('Authorization'), key='ananth1404', algorithms='HS256')
            userdata = UsersData.load(id=decoded['email'], db=server['users_data'])
            if userdata is not None:
                db = server['tts_data']
                response = db.get(id='list_language')
                del response['_id']
                del response['_rev']
                return response
            else:
                response = {
                    'message': 'UserNotFound'
                }
                return response, 404

        except jwt.exceptions.InvalidTokenError:
            abort(
                http_status_code=401,
                message='Invalid Token'
            )

        except jwt.exceptions.InvalidSignatureError:
            abort(
                http_status_code=401,
                message='Invalid Signature'
            )

        except jwt.exceptions.ExpiredSignatureError:
            abort(
                http_status_code=401,
                message='Expired Signature'
            )

class History(Resource):
    pass

class TTS(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='Authorization', location='headers', required=True, trim=True, type=str)
        parser.add_argument(name='lang', location='json', required=True, trim=True, type=str)
        parser.add_argument(name='text', location='json', required=True, trim=True, type=str)
        args = parser.parse_args(strict=True)
        try:
            decoded = jwt.decode(jwt=args.get('Authorization'), key='ananth1404', algorithms='HS256')
            userdata = UsersData.load(id=decoded['email'], db=server['users_data'])
            if userdata is not None:
                history = HistoryData(
                    client_id = userdata.client_id,
                    text = args.get('text'),
                    language = args.get('lang')
                )
                threading.Thread(
                    target = history.store(db=server['history_data'])
                )
                text = translator(
                    text = args.get('text'),
                    lang = args.get('lang')[0:5]
                )
                userdata.wallet = userdata.wallet - userdata.per_request
                response = Response(
                    response = tts(language=args.get('lang'), text=text),
                    mimetype = 'audio/x-wav'
                )
                threading.Thread(
                    target = userdata.store(db=server['users_data'])
                )
                return response
            else:
                response = {
                    'message': 'UserNotFound'
                }
                return response, 404

        except jwt.exceptions.InvalidTokenError:
            abort(
                http_status_code=401,
                message='Invalid Token'
            )

        except jwt.exceptions.InvalidSignatureError:
            abort(
                http_status_code=401,
                message='Invalid Signature'
            )

        except jwt.exceptions.ExpiredSignatureError:
            abort(
                http_status_code=401,
                message='Expired Signature'
            )