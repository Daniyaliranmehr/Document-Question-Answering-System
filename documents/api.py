from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Document

@api_view(['GET'])
def list_documents(request):
    docs = Document.objects.all().values()
    return Response(docs)