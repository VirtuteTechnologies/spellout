from flask import Flask
from flask_restful import Api

# userdefined Modules
from spellout.config import Config
from spellout.common.utils import mail
from spellout.resources.tts import ListLanguages, TTS
from spellout.resources.user import User, ChangePassword
from spellout.resources.register import UserRegistration, Verification, Resend
from spellout.resources.authenticate import Authenticate, ForgotPassword, VerifyForgotPassword, Login


app = Flask(__name__)
api = Api(app=app, prefix='/v1')
app.config.from_object(obj=Config)
mail.init_app(app=app)

# Resources
api.add_resource(TTS, '/tts')
api.add_resource(User, '/user')
api.add_resource(Login, '/login')
api.add_resource(Resend, '/resend')
api.add_resource(Verification, '/verify')
api.add_resource(UserRegistration, '/signup')
api.add_resource(Authenticate, '/authenticate')
api.add_resource(ListLanguages, '/list_languages')
api.add_resource(ForgotPassword, '/forgot_password')
api.add_resource(ChangePassword, '/change_password')
api.add_resource(VerifyForgotPassword, '/verify_forgot_password')