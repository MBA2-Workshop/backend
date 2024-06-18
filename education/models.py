from django.utils import timezone
from django.db import models


class Training(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    cfa = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="training_cfa")
    instructor = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="training_instructor", null=True, blank=True)
    students = models.ManyToManyField("user.User", related_name="training_students", null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now, blank=True)
    end_date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.name} [{self.start_date.year} - {self.end_date.year}]"
