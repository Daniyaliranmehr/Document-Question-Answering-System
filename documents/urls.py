from django.urls import path
from .views import (
    DocumentListView,
    DocumentDetailView,
    DocumentUploadView,
    DocumentUpdateView,
)

urlpatterns = [
    path('', DocumentListView.as_view(), name='document-list'),
    path('<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('<int:pk>/update/', DocumentUpdateView.as_view(), name='document-update')
]