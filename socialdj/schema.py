import graphene

import feed.schema as fch
import accounts.schema as ach

class Query(fch.Query, ach.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)