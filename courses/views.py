from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from elasticsearch_dsl import Q
from .models import Course, Category, Tag
from .serializers import CourseSerializer, CourseCreateSerializer, CategorySerializer, TagSerializer
from .search_indexes import CourseDocument

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.filter(status='published')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'instructor']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'title']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]  # Only instructor or admin can modify
        return [IsAuthenticatedOrReadOnly()]

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

@api_view(['GET'])
def search_courses(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Elasticsearch search
    from elasticsearch_dsl.connections import connections
    connections.create_connection(hosts=['localhost:9200'])
    from .search_indexes import CourseDocument

    search = CourseDocument.search()
    search = search.query(
        Q('multi_match', query=query, fields=['title', 'description', 'instructor_name', 'tags'])
    )

    results = []
    for hit in search.execute():
        course = Course.objects.get(id=hit.meta.id)
        results.append(CourseSerializer(course).data)

    return Response(results)

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.filter(status='published')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'instructor']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'title']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseCreateSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]  # Only instructor or admin can modify
        return [IsAuthenticatedOrReadOnly()]

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
