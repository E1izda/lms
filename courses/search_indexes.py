from elasticsearch_dsl import Document, Text, Keyword, Integer, Float
from elasticsearch_dsl.connections import connections
from .models import Course


class CourseDocument(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    description = Text(analyzer='snowball')
    instructor_name = Text()
    category_name = Text()
    tags = Keyword(multi=True)
    difficulty = Keyword()
    price = Float()
    status = Keyword()

    class Index:
        name = 'courses'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    def save(self, **kwargs):
        return super().save(**kwargs)

def bulk_indexing():
    connections.create_connection(hosts=['localhost:9200'])
    CourseDocument.init()
    for course in Course.objects.filter(status='published'):
        doc = CourseDocument(
            meta={'id': course.id},
            title=course.title,
            description=course.description,
            instructor_name=course.instructor.get_full_name(),
            category_name=course.category.name if course.category else '',
            tags=[tag.name for tag in course.tags.all()],
            difficulty=course.difficulty,
            price=float(course.price),
            status=course.status
        )
        doc.save()