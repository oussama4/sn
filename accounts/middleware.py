from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import jwt

class JwtMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = get_auth_token(request)
        if token is not None:
            if not hasattr(request, 'user') or request.user.is_anonymous:
                try:
                    dec = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                except jwt.exceptions.InvalidTokenError:
                    return JsonResponse({
                        'auth_error': 'invalid token'
                    })
                else:
                    User = get_user_model()
                    request.user = User.objects.get(pk=dec.get('id'))

def get_auth_token(request):
    header = request.META.get('HTTP_AUTHORIZATION', '').split()
    if len(header) != 2:
        return None
    return header[1]