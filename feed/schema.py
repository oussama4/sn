import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.contenttypes.models import ContentType

from feed.models import Action, Post, Comment
from accounts.models import User

class ActionType(DjangoObjectType):
    class Meta:
        model = Action

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class ActionInput(graphene.InputObjectType):
    verb = graphene.String()
    post = graphene.Int()
    target_actor = graphene.Int()

class CommentInput(graphene.InputObjectType):
    action = graphene.Int()
    body = graphene.String()

# a mutaion that creates action objects
class CreateAction(graphene.Mutation):
    class Arguments:
        action = graphene.NonNull(ActionInput)
    
    id = graphene.Int()
    verb = graphene.String()

    def mutate(self, info, action):
        target_act = User.objects.get(pk=action.target_actor)
        post = Post.objects.get(pk=action.post)
        a = Action.objects.create(actor=info.context.user, 
                                  verb=action.verb, target=post, target_actor=target_act)
        return CreateAction(id=a.id, verb=a.verb)

# a mutation that creates comment objects
class CreateComment(graphene.Mutation):
    class Arguments:
        comment = graphene.NonNull(CommentInput)

    id = graphene.Int()

    def mutate(self, info, comment):
        a = Action.objects.get(pk=comment.action)
        c = Comment.objects.create(user=info.context.user, action=a, body=comment.body)
        return CreateComment(id=c.id)

class Query(object):
    actions = graphene.List(ActionType,
                            limit=graphene.NonNull(graphene.Int),
                            offset=graphene.NonNull(graphene.Int),
                            is_profile=graphene.NonNull(graphene.Boolean),
                            user_id=graphene.Int())
    posts = graphene.List(PostType)
    comments = graphene.List(CommentType)

    def resolve_actions(self, info, **kwargs):
        limit = kwargs.get('limit')
        offset = kwargs.get('offset')
        is_profile = kwargs.get('is_profile')
        if is_profile:
            user_id = kwargs.get('user_id')
            return Action.objects.filter(
                    actor_id=user_id
                    ).prefetch_related('comments').select_related('actor', 'target')[offset:limit]
        qs = list(info.context.user.is_following.all())
        qs.append(info.context.user)
        return Action.objects.filter(
                    actor__in=qs
                    ).prefetch_related('comments').select_related('actor', 'target')[offset:limit]

    def resolve_posts(self, info, **kwargs):
        return Post.objects.all()

    def resolve_comments(self, info, **kwargs):
        return Comment.objects.all()

class Mutation(graphene.ObjectType):
    create_action = CreateAction.Field()
    create_comment = CreateComment.Field()
    