from datetime import datetime, timedelta

import graphene
from graphene_django.types import DjangoObjectType
from django.conf import settings
from django.contrib.auth import authenticate
import jwt

from .models import User, OfpptID

class UserType(DjangoObjectType):
    class Meta:
        model = User

class LoginInput(graphene.InputObjectType):
    email = graphene.String()
    password = graphene.String()

class LoginOutput(graphene.ObjectType):
    errored = graphene.Boolean()
    errors = graphene.String()
    user = graphene.Field(UserType)
    token = graphene.String()

class Query(object):
    users = graphene.List(UserType)
    user = graphene.Field(UserType,
                          user_id=graphene.NonNull(graphene.Int))

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        return User.objects.get(pk=user_id)

class Login(graphene.Mutation):
    class Arguments:
        input = graphene.NonNull(LoginInput)

    output = graphene.Field(LoginOutput)

    def mutate(self, info, input):
        u = authenticate(info.context, username=input.email, password=input.password)
        if u is None:
            out = LoginOutput(errored=True,
                              errors='invalid credencials',
                              user=None,
                              token='')
            return Login(output=out)
        else:
            tk = jwt.encode({
                        'id': u.id,
                        'exp': datetime.utcnow() + timedelta(days=1)
                    },
                    settings.SECRET_KEY,
                    algorithm='HS256')
            out = LoginOutput(errored=False,
                              errors='',
                              user=u,
                              token=tk)
            return Login(output=out)

class Mutation(graphene.ObjectType):
    token_auth = Login.Field()
