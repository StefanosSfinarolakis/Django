from django.db import models

# Create your models here.

##LIB##
from django.contrib.auth import get_user_model


User = get_user_model()

##prof##
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()

#    def __str__(self):
#       return self.user.username



#ftaixnei profile me user kai user id