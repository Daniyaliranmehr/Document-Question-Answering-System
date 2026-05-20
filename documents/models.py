from django.db import models
from .utils import extract_text_from_docx


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.file.name.endswith('.docx'):
            self.content = extract_text_from_docx(self.file.path)

        super().save(update_fields=['content'])

    def __str__(self):
        return self.title