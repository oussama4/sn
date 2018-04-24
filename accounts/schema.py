from django.core.exceptions import ObjectDoesNotExist, ValidationError
import graphene
from graphene_django.types import DjangoObjectType

from .models import User, OfpptID
from .validators import validate_password

class UserType(DjangoObjectType):
    class Meta:
        model = User

class RegisterError(graphene.ObjectType):
    can_register = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()

class RegisterOutput(graphene.ObjectType):
    user = graphene.Field(UserType)
    errored = graphene.Boolean()
    errors = graphene.Field(RegisterError)

class RegisterInput(graphene.InputObjectType):
    ofppt = graphene.NonNull(graphene.String)
    email = graphene.NonNull(graphene.String)
    first_name = graphene.NonNull(graphene.String)
    last_name = graphene.NonNull(graphene.String)
    password = graphene.NonNull(graphene.String)
    password2 = graphene.NonNull(graphene.String)

class Query(object):
    users = graphene.List(UserType)
    user = graphene.Field(UserType,
                          user_id=graphene.NonNull(graphene.Int))

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, **kwargs):
        user_id = kwargs.get('user_id')
        return User.objects.get(pk=user_id)
