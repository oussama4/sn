import graphene
from graphene_django.types import DjangoObjectType

from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(object):
    users = graphene.List(UserType)
    user = graphene.Field(UserType,
                          user_id=graphene.NonNull(graphene.Int))

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        return User.objects.get(pk=user_id)