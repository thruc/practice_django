import graphene
import employees.schema
import users.schema


class Query(users.schema.Query, employees.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, employees.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)