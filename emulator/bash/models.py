from django.db import models

# Create your models here.
class command_response(models.Model):
    command=models.TextField(blank=True,default="")
    response=models.TextField(blank=True,default="")

    def __str__(self):
        return self.command
    