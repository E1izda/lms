
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/courses/', include('courses.urls')),
    path('api/v1/lessons/', include('lessons.urls')),
    path('api/v1/quizzes/', include('quizzes.urls')),
    path('api/v1/progress/', include('progress.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/reviews/', include('reviews.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/recommendations/', include('recommendations.urls')),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
