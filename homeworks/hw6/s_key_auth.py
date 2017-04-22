# import the User object
from django.contrib.auth.models import User
import hashlib, binascii


class S_KEY_backend:
    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):

        try:
            # Try to find a user matching your username
            user = User.objects.get(username=username)

            password = password.encode('ascii')

            dk = hashlib.pbkdf2_hmac('sha256', password, b'salt', 100000)
            hashed_pass = binascii.hexlify(dk)

            #  Check the password is the reverse of the username
            if user.check_password(hashed_pass):
                user.set_password(password)
                user.save()
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except User.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
