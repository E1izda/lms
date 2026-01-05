from django.urls import path
from .views import get_recommendations

app_name = 'recommendations'

urlpatterns = [
    path('', get_recommendations, name='get-recommendations'),
]