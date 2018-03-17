import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.contenttypes.models import ContentType

from feed.models import Action, Post
from accounts.models import User

class ActionType(DjangoObjectType):
    class Meta:
        model = Action

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class ActionInput(graphene.InputObjectType):
    verb = graphene.String()
    post = graphene.Int()
    target_actor = graphene.Int()

# a mutaion that creates action objects
class CreateAction(graphene.Mutation):
    class Arguments:
        action = ActionInput()
    
    id = graphene.Int()
    verb = graphene.String()

    def mutate(self, info, action):
        target_act = User.objects.get(pk=action.target_actor)
        post = Post.objects.get(pk=action.post)
        a = Action.objects.create(actor=info.context.user, 
                                  verb=action.verb, target=post, target_actor=target_act)
        return CreateAction(id=a.id, verb=a.verb)

class Query(object):
    actions = graphene.List(ActionType,
                            limit=graphene.NonNull(graphene.Int),
                            offset=graphene.NonNull(graphene.Int),
                            is_profile=graphene.NonNull(graphene.Boolean),
                            user_id=graphene.Int())
    posts = graphene.List(PostType)

    def resolve_actions(self, info, **kwargs):
        limit = kwargs.get('limit')
        offset = kwargs.get('offset')
        is_profile = kwargs.get('is_profile')
        if is_profile:
            user_id = kwargs.get('user_id')
            return Action.objects.filter(
                    actor_id=user_id).select_related('actor', 'target')[offset:limit]
        qs = list(info.context.user.is_following.all())
        qs.append(info.context.user)
        return Action.objects.filter(
                    actor__in=qs
                    ).select_related('actor', 'target')[offset:limit]

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

class Mutation(graphene.ObjectType):
    create_action = CreateAction.Field()
    