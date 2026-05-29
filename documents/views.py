from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Document
from .serializers import DocumentSerializer
from .utils import extract_text

from django.shortcuts import get_object_or_404

from django.shortcuts import render


class DocumentListView(APIView):
    """
    List all documents.

    This endpoint returns all documents stored in the system.
    It is used for displaying document lists in the frontend or admin panels.
    """

    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class DocumentDetailView(APIView):
    """
    Retrieve a single document by ID.

    This endpoint returns detailed information about a specific document.
    It is useful for viewing or processing a single document in the system.
    """

    def get(self, request, pk):
        try:
            document = Document.objects.get(id=pk)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DocumentSerializer(document)
        return Response(serializer.data)


class DocumentUploadView(APIView):
    """
    Upload a new document.

    This endpoint allows users to upload a document file along with metadata.
    After saving the file, its text content is extracted (if supported)
    and stored in the database for further processing (e.g., RAG pipeline).
    """

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)

        if serializer.is_valid():
            document = serializer.save()

            if document.file.name.endswith('.docx'):
                document.content = extract_text(document.file.path)
                document.save(update_fields=['content'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DocumentUpdateView(APIView):
    """
    Update an existing document.

    This endpoint allows updating the document title 
    or replacing the uploaded file.
    """

    def patch(self, request, pk):
        document = get_object_or_404(Document, pk=pk)

        serializer = DocumentSerializer(
            document,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            document = serializer.save()

            if 'file' in request.FILES:
                document.content = extract_text(document.file.path)
                document.save(update_fields=['content'])

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DocumentDeleteView(APIView):
    """
    Delete a document.

    This endpoint removes a document from the database permanently.
    """

    def delete(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        document.delete()

        return Response(
            {"message": "Document deleted successfully."},
            status=status.HTTP_200_OK
        )
    

def home(request):
    """
    Render the home page template.
    """
    return render(request, 'index.html')