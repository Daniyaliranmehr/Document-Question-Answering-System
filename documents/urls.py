from django.urls import path
from .views import (
    list_documents,
    get_document,
    delete_document
)


urlpatterns = [
    path('', list_documents),
    path('<int:document_id>/', get_document),
    path('delete/<int:document_id>/', delete_document)
]