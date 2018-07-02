import jwt
import datetime
from passlib.apps import custom_app_context as pwd_context

class User(object):
    def __init__(self):
        self.email = 'cookie@gmail.com'
        self.password = self.hash_password('123456789')
        self.create_time = datetime.datetime.now()
        self.status = 0
        
    def hash_password(self, password):
        return pwd_context.encrypt(password + 'SECRET_KEY')
    
    def verify_password(self, password):
        return pwd_context.verify(
            password + 'SECRET_KEY', self.password)
    
    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(hours=6, seconds=0),
                'iat': datetime.datetime.now(),
                'sub': self.email 
            }
            return jwt.encode(
                payload,
                'SECRET_KEY',
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
    def decode_auth_token(self,auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, 'SECRET_KEY')
            print(payload)
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

if __name__ == '__main__':
    user = User()
    token = user.encode_auth_token()
    print(token)
    user.decode_auth_token(token)