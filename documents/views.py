from django.http import JsonResponse
from .models import Document
from django.shortcuts import get_object_or_404


def list_documents(request):

    documents = Document.objects.all()

    data = []

    for doc in documents:
        data.append({
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "created_at": doc.created_at,
        })

    return JsonResponse(data, safe=False)


def get_document(request, document_id):

    doc = get_object_or_404(Document, id=document_id)

    data = {
        "id": doc.id,
        "title": doc.title,
        "content": doc.content,
        "created_at": doc.created_at,
    }

    return JsonResponse(data)