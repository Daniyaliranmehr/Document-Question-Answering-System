from django.urls import path
from .views import list_documents, get_document

urlpatterns = [
    path('', list_documents),
    path('<int:document_id>/', get_document)
]