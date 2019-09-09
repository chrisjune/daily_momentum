import graphene

from graphene_django.types import DjangoObjectType

from todo.models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo

class Query:
    all_todos = graphene.List(TodoType)

    def resolve_all_todos(self, info, **kwargs):
        return Todo.objects.all()
