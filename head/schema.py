import graphene
from graphene_django import DjangoObjectType
from courses.models import Course
from users.models import User

class CourseType(DjangoObjectType):
    class Meta:
        model = Course

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    all_courses = graphene.List(CourseType)
    course = graphene.Field(CourseType, id=graphene.Int())

    def resolve_all_courses(self, info):
        return Course.objects.filter(status='published')

    def resolve_course(self, info, id):
        return Course.objects.get(pk=id)

schema = graphene.Schema(query=Query)