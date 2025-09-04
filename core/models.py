from django.db import models

# Create your models here.

class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=200, unique=True)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
