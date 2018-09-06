import graphene

import feed.schema as fch
import accounts.schema as ach
import chat.schema as cch

class Query(fch.Query, ach.Query, cch.Query, graphene.ObjectType):
    pass

class Mutation(fch.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)