import os
import random
import threading
from datetime import datetime
from flask_restful import Resource, reqparse, abort, fields, marshal_with

# user-defined modules
from spellout.common.models import UsersData, server

# Environment Variables
# database = os.environ['USERS_DATABASE']


class UserRegistration(Resource):
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='email', type=str, location='args', default=None, trim=True)
        args = parser.parse_args(
            strict=True
        )
        userdata = UsersData.load(id=args.get('email'), db=server['users_data'])
        if userdata is not None:
            return {
                'message': 'User Already Present'
            }, 200
        else:
            abort(
                http_status_code = 404,
                message = 'UserNotFound'
            )
    
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='first_name', type=str, location='json', required=True, trim=True)
        parser.add_argument(name='last_name', type=str, location='json', required=True, trim=True)
        parser.add_argument(name='organization', type=str, location='json', required=True, trim=True)
        parser.add_argument(name='email', type=str, location='json', required=True, trim=True)
        parser.add_argument(name='phone_number', type=str, location='json', required=True, trim=True)
        parser.add_argument(name='passcode', type=str, location='json', required=True, trim=True, dest='passcode')
        args = parser.parse_args(strict=True)
        try:
            rand = random.randint(a=000000, b=999999)
            print(rand)
            userdata = UsersData(
                first_name = args.get('first_name'),
                last_name = args.get('first_name'),
                organization = args.get('first_name'),
                id = args.get('email'),
                phone_number = args.get('phone_number'),
                password = args.get('passcode'),
                verification_code = rand
            )
            userdata.store(db=server['users_data'])

            return {
                'status': 'Email Sent',
                'email': userdata.id,
                'code': rand
            }
        except:
            abort(
                http_status_code=400,
                message = 'UserAlreadyFound'
            )

class Verification(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='verification_code', required=True, location='json', type=str, trim=True)
        parser.add_argument(name='email', type=str, location='json', required=True, trim=True)
        args = parser.parse_args(strict=True)
        userdata = UsersData.load(id=args.get('email'), db=server['users_data'])
        if userdata is not None:
            if args.get('verification_code') == userdata.verification_code:
                userdata.email_verified = True
                userdata.verification_code = None
                userdata.last_modified = datetime.now()
                userdata.store(db=server['users_data'])
                return {
                    'message': 'success'
                }
            else: 
                return abort(
                    http_status_code = 401,
                    message = 'Invalid Code'
                )
        
        else:
            abort(
                http_status_code = 404,
                message = 'UserNotFound'
            )

class Resend(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='email', type=str, location='json', required=True, trim=True)
        args = parser.parse_args(strict=True)
        userdata = UsersData.load(id=args.get('email'), db=server['users_data'])
        if userdata is not None:
            print(userdata.verification_code)
            return {
                'message': 'sent'
            }
        else:
            abort(
                http_status_code=404,
                message = 'UserNotFound'
            )