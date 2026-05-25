from django.contrib import admin
from .models import QARecord
from .rag import rag_pipeline

@admin.register(QARecord)
class QARecordAdmin(admin.ModelAdmin):
    list_display = ("question", "answer", "created_at")
    readonly_fields = ("answer", "created_at")  # answer is auto-generated
    fields = ("question", "answer", "created_at")

    def save_model(self, request, obj, form, change):
        """
        When a question is saved, the RAG pipeline runs and populates answer.
        """
        if not obj.answer:  # only if answer is empty
            obj.answer = rag_pipeline(obj.question)
        super().save_model(request, obj, form, change)