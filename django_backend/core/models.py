from django.db import models
import uuid
from datetime import datetime

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    caption = models.TextField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name