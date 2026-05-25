from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Document
from .serializers import DocumentSerializer
from .utils import extract_text_from_docx

from django.shortcuts import get_object_or_404


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
                document.content = extract_text_from_docx(document.file.path)
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
        # 1. Get document or return 404 if not found
        document = get_object_or_404(Document, pk=pk)

        # 2. Apply partial update
        serializer = DocumentSerializer(
            document,
            data=request.data,
            partial=True
        )

        # 3. Validate input data
        if serializer.is_valid():

            # 4. Save updated fields
            document = serializer.save()

            # 5. If file is updated, re-extract content
            if 'file' in request.FILES:
                document.content = extract_text_from_docx(document.file.path)
                document.save(update_fields=['content'])

            # 6. Return updated object
            return Response(serializer.data, status=status.HTTP_200_OK)

        # 7. If validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)