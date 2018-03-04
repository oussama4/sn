import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.contenttypes.models import ContentType

from feed.models import Action, Post

class ActionType(DjangoObjectType):
    class Meta:
        model = Action

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CtType(DjangoObjectType):
    class Meta:
        model = ContentType

class Query(object):
    actions = graphene.List(ActionType,
                            limit=graphene.NonNull(graphene.Int),
                            offset=graphene.NonNull(graphene.Int))
    ctypes = graphene.List(CtType)
    posts = graphene.List(PostType)

    def resolve_actions(self, info, **kwargs):
        limit = kwargs.get('limit')
        offset = kwargs.get('offset')
        return Action.objects.select_related('actor', 'target_ct')[offset:limit]

    def resolve_ctypes(self, info, **kwargs):
        return ContentType.objects.all()

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()