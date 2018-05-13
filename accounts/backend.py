from django.contrib.auth import get_user_model

User = get_user_model()

class JwtBackend:
    def authenticate(self, request, username, password):
        try:
            u = User.objects.get(email=username)
        except User.DoesNotExist:
            return None
        else:
            if u.check_password(password):
                return u
            return None

    def get_user(self, user_id):
        try:
            u = User.objects.get(pk=user_id)
            return u
        except User.DoesNotExist:
            return None