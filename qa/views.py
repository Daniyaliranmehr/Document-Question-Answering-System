from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuestionSerializer
from .rag import rag_pipeline

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class AskQuestionView(APIView):

    authentication_classes = []
    permission_classes = []

    """
    Answer user questions using the RAG pipeline.

    This endpoint receives a question,
    retrieves relevant document chunks,
    and generates an answer using the LLM.
    """

    def post(self, request):

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid():

            question = serializer.validated_data['question']

            answer = rag_pipeline(question)

            return Response(
                {
                    "question": question,
                    "answer": answer
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )