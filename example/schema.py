import graphene
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphene import ObjectType, Schema
from graphene_file_upload.scalars import Upload


class UploadMutation(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    content = graphene.String()

    def mutate(self, info, file: InMemoryUploadedFile, **kwargs):
        with file.open('rb') as fd:
            content = fd.read().decode('utf8')

        return UploadMutation(success=True, content=content)


class QueryRoot(ObjectType):

    test = graphene.String(who=graphene.String())

    def resolve_test(self, info):
        return "Hello World"


class Mutation(ObjectType):
    test_file_upload = UploadMutation.Field()
    test = graphene.Field(QueryRoot)


schema = Schema(query=QueryRoot, mutation=Mutation)
