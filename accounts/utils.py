from django.conf import settings
from django.contrib.auth import get_user_model
import jwt

def get_user_by_token(token):
    if token is not None:
        try:
            dec = jwt.decode(str(token), settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError as ex:
            return None
        else:
            User = get_user_model()
            return User.objects.get(pk=dec.get('id'))
    else:
        return None

def get_auth_token(request):
    header = request.META.get('HTTP_AUTHORIZATION', '').split()
    if len(header) != 2:
        return None
    return header[1]