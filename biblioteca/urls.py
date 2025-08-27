from django.urls import path, include
from .views import LibroListView

urlpatterns = [
    path('biblioteca/', LibroListView.as_view(), name='libro-lista'),
]