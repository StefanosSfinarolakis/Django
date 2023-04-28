from django.db import models

class Image(models.Model):
    name = models.CharField(max_length=100)
    caption = models.TextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name