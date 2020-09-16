import os
import jwt
from datetime import datetime
from flask_restful import reqparse, abort, Resource, marshal_with, fields

# userdefined Modules
from spellout.common.models import UsersData, server

output = {
    'email': fields.String(attribute='email'),
    'cliend_id': fields.String(attribute='client_id'),
    'client_secret': fields.String(attribute='client_secret'),
    'first_name': fields.String(attribute='first_name'),
    'last_name': fields.String(attribute='last_name'),
    'wallet': fields.String(attribute='wallet'),
    'phone_number': fields.String(attribute='phone_number'),
    'organization': fields.String(attribute='organization'),
    'last_login': fields.DateTime(dt_format='rfc822', attribute='last_login'),
    'last_modified': fields.DateTime(dt_format='rfc822', attribute='last_modified'),
    'created_on': fields.DateTime(dt_format='rfc822', attribute='created_on'),
}


class User(Resource):
    @marshal_with(fields=output)
    def get(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='Authorization', required=True, location='headers', trim=True, type=str)
        args = parser.parse_args(strict=True)
        try:
            decoded = jwt.decode(jwt=args.get('Authorization'), key='ananth1404', algorithms='HS256')
            userdata = UsersData.load(id=decoded['email'], db=server['users_data'])
            output = {
                'email': userdata.id,
                'first_name': userdata.first_name,
                'last_name': userdata.last_name,
                'phone_number': userdata.phone_number,
                'organization': userdata.organization,
                'last_login': userdata.last_login,
                'last_modified': userdata.last_modified,
                'wallet': userdata.wallet,
                'client_id': userdata.client_id,
                'client_secret': userdata.client_secret,
                'created_on': userdata.created_on
            }
            return output
        
        except jwt.exceptions.InvalidTokenError:
            abort(
                http_status_code = 404,
                message = 'Invalid Token'
            )

        except jwt.exceptions.InvalidSignatureError:
            abort(
                http_status_code = 404,
                message = 'Invalid Signature'
            )

        except jwt.exceptions.ExpiredSignatureError:
            abort(
                http_status_code = 403,
                message = 'Expired Signature'
            )
    
    def delete(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='Authorization', required=True, type=str, location='headers', trim=True)
        args = parser.parse_args(strict=True)
        try:
            decoded = jwt.decode(jwt=args.get('Authorization'), key='ananth1404', algorithms='HS256')
            db = server['users_data']
            userdata = db.get(id=decoded['email'])
            if userdata is not None:
                db.delete(doc=userdata)
                response = {
                    'message': 'deleted'
                }
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
    
    def put(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='Authorization', required=True, location='headers', trim=True)
        parser.add_argument(name='first_name', type=str, location='json', required=False, trim=True)
        parser.add_argument(name='last_name', type=str, location='json', required=False, trim=True)
        parser.add_argument(name='organization', type=str, location='json', required=False, trim=True)
        parser.add_argument(name='email', type=str, location='json', required=False, trim=True)
        parser.add_argument(name='phone_number', type=str, location='json', required=False, trim=True)
        args = parser.parse_args(strict=True)
        try:
            decoded = jwt.decode(jwt=args.get('Authorization'), key='ananth1404', algorithms='HS256')
            userdata = UsersData.load(id=decoded['email'], db=server['users_data'])
            if userdata is not None:
                del args['Authorization']
                for x, y in args.items():
                    if y is not None:
                        userdata[x] = y
                userdata.last_modified = datetime.now()
                userdata.store(db=server['users_data'])
                return {
                    'message': 'success'
                }
            else:
                response = {
                    'message': 'UserNotFound'
                }
                return response,  404

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

class ChangePassword(Resource):
    def put(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(name='Authorization', required=True, location='headers', trim=True)
        parser.add_argument(name='old_password', required=True, location='json', trim=True)
        parser.add_argument(name='new_password', required=True, location='json', trim=True)
        args = parser.parse_args(strict=True)
        try:
            decoded = jwt.decode(jwt=args.get('Authorization'), key='ananth1404', algorithms='HS256')
            userdata = UsersData.load(id=decoded['email'], db=server['users_data'])
            if userdata is not None:
                if userdata.password == args.get('old_password'):
                    userdata.password = args.get('new_password')
                    userdata.last_modified = datetime.now()
                    userdata.store(db=server['users_data'])
                    return {
                        'message': 'Password Changed'
                    }
                else:
                    response = {
                        'message': 'Invalid Password'
                    }
                    return response, 401
            else:
                response = {
                    'message': 'UserNotFound'
                }
                return response, 404

        
        except jwt.exceptions.InvalidTokenError:
            abort(
                http_status_code = 401,
                message = 'Invalid Token'
            )

        except jwt.exceptions.InvalidSignatureError:
            abort(
                http_status_code = 401,
                message = 'Invalid Signature'
            )

        except jwt.exceptions.ExpiredSignatureError:
            abort(
                http_status_code = 401,
                message = 'Expired Signature'
            )
