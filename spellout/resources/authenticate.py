import os
import random
import datetime
import threading
from flask_restful import Resource, reqparse, abort, fields, marshal_with

# user defined modules
from spellout.common.models import UsersData, server
from spellout.common.utils import encoding, send_mail

# Response
access_token_fields = {
    'Access Token': fields.String(attribute='access_token')
}


class Authenticate(Resource):
    @marshal_with(fields=access_token_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='client_id', type=str, required=True, location='json', trim=True)
        parser.add_argument(name='client_secret', type=str, required=True, location='json', trim=True)
        args = parser.parse_args()
        query = {
            'selector': {
                'client_id': args.get('client_id'),
                'client_secret': args.get('client_secret')
            },
            'fields': ['client_id', '_id']
        }
        res = server['users_data'].find(query)
        res = list(res)
        if len(list(res)) == 1:
            access_token = encoding(client_id=args.get('client_id'), email = res[0].get('_id'))
            return {
                'access_token': access_token
            }
        else:
            abort(
                http_status_code = 401,
                message = 'invalid Credentails'
            )

class Login(Resource):
    def post(self):
        pass

class ForgotPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='email', type=str, required=True, location='json', trim=True)
        args = parser.parse_args()
        userdata = UsersData.load(id=args.get('email'), db=server['users_data'])
        if userdata is not None:
            rand = random.randint(a=000000, b=999999)
            userdata.verification_code = rand
            userdata.store(db=server['users_data'])
            return {
                'message': 'success',
                'code': rand
            }
        else:
            abort(
                http_status_code = 404,
                message = 'UserNotFound'
            )


class VerifyForgotPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='email', type=str, required=True, location='json', trim=True)
        parser.add_argument(name='verification_code', type=str, required=True, location='json', trim=True)
        parser.add_argument(name='password', type=str, required=True, location='json', trim=True)
        args = parser.parse_args()
        userdata = UsersData.load(id=args.get('email'), db=server['users_data'])
        if userdata is not None:
            if args.get('verification_code') == userdata.verification_code:
                userdata.verification_code = None
                userdata.last_modified = datetime.now()
                userdata.password = args.get('password')
                userdata.store(db=server['users_data'])
            else:
                abort(
                    http_status_code = 401,
                    message = 'Invalid Code'
                )
        else:
            abort(
                http_status_code = 404,
                message = 'UserNotFound'
            )