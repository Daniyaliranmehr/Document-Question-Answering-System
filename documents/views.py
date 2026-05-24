from django.http import JsonResponse
from .models import Document

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