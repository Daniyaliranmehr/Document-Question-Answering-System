from django.db import models
from .utils import extract_text


class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new and self.file:
            self.content = extract_text(self.file.path)
            super().save(update_fields=['content'])

    def __str__(self):
        return self.title