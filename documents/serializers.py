from rest_framework import serializers
from .models import Document
import os


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file', 'content', 'created_at']
        read_only_fields = ['content', 'created_at']


def validate_file(self, value):
    allowed_extensions = ['.docx', '.txt']

    extension = os.path.splitext(value.name)[1].lower()

    if extension not in allowed_extensions:
        raise serializers.ValidationError(
            "Only DOCX, PDF, and TXT files are supported."
        )

    return value