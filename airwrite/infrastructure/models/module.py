from django.db import models


class Module(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=200, unique=True)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'core'  # keep migrations and DB table under 'core'

    def __str__(self):
        return self.name