from django.urls import path
from .views import list_documents

urlpatterns = [
    path('', list_documents),
]