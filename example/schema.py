import graphene
from graphene import ObjectType, Schema


class QueryRoot(ObjectType):

    test = graphene.String(who=graphene.String())

    def resolve_test(self, info):
        return "Hello World"


schema = Schema(query=QueryRoot)
