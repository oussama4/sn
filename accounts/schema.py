import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType

from .models import User, OfpptID

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

class Login(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info):
        return cls(user=info.context.user)

class Mutation(graphene.ObjectType):
    token_auth = Login.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
