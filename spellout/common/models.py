import os
import uuid
import string
import random
from couchdb import Server
from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, IntegerField, BooleanField

# Environment Variables
# url = os.environ['COUCHDB_SERVER']
server = Server(url=r"http://admin:admin@15.206.127.10:5984/")


def secret_key():
    N = 20
    secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N)) 
    return secret

class UsersData(Document):
    email = TextField(name='id')
    first_name = TextField(name='first_name')
    last_name = TextField(name='last_name')
    organization = TextField(name='organization')
    password = TextField(name='passcode')
    phone_number = TextField(name='phone_number')
    wallet = IntegerField(name='wallet', default=100)
    per_request = IntegerField(name='per_requests', default=1)
    status = TextField(name='status', default='active')
    email_verified = TextField(name='email_verified', default=False)
    created_on = DateTimeField(default=datetime.now)
    last_modified = DateTimeField(default=datetime.now, name='last_modified')
    last_login = DateTimeField(default=datetime.now, name='last_login')
    client_id = TextField(default=uuid.uuid4)
    client_secret = TextField(name='client_secret', default=secret_key)
    verification_code = TextField(name='verification_code')

    def __str__(self):
        return self._rev

class HistoryData(Document):
    client_id = TextField(name='client_id')
    text = TextField(name='text')
    language = TextField(name='language')
    created_on = DateTimeField(name='created_on', default=datetime.now)

    def __str__(self):
        return id