from django.db import models


class Example(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def deactivate(self):
        self.is_active = False
        self.save()
