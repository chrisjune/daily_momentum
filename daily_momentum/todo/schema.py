import graphene

from graphene_django.types import DjangoObjectType

from todo.models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo

class TodoInsertMutation(graphene.Mutation):
    class Arguments:
        contents = graphene.String()

    ok = graphene.Boolean()    
    todo = graphene.Field(TodoType)

    def mutate(root, info, contents):
        todo = Todo(contents=contents)
        todo.save()
        ok = True
        return TodoInsertMutation(todo=todo, ok=ok)


class TodoInput(graphene.InputObjectType):
    contents = graphene.String(required=True)
    pk = graphene.Int(required=True)


class TodoUpdateMutation(graphene.Mutation):
    class Arguments:
        todo_data = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(TodoType)

    def mutate(root, info, todo_data):
        ok = True
        todo = Todo.objects.filter(pk=todo_data.pk).first()
        todo.contents = todo_data.contents
        todo.save()
        return TodoUpdateMutation(todo=todo, ok=ok)

class TodoDeleteMutation(graphene.Mutation):
    class Arguments:
        pk = graphene.Int(required=True)

    ok = graphene.Boolean()
    def mutate(root, info, pk):
        todo = Todo.objects.filter(pk=pk)
        todo.delete()
        ok = True
        return TodoDeleteMutation(ok=ok)

class Query:
    all_todos = graphene.List(TodoType)

    def resolve_all_todos(self, info, **kwargs):
        return Todo.objects.all()

class Mutation(graphene.ObjectType):
    insert_todo = TodoInsertMutation.Field()
    update_todo = TodoUpdateMutation.Field()
    delete_todo = TodoDeleteMutation.Field()
