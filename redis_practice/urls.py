from django.urls import path
from .views import RedisOperations

urlpatterns = [
    path('data/', RedisOperations.as_view(), name='redis_data_ops'),
]
