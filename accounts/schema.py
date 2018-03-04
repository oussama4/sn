import graphene
from graphene_django.types import DjangoObjectType

from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(object):
    users = graphene.List(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()