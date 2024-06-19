from django.utils import timezone
from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=255)
    comment = models.TextField()
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="label")
    student = models.ForeignKey("user.User", related_name="training_students", null=True,
                                blank=True, on_delete=models.CASCADE)
    coefficient = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.name} [{self.value} - {self.coefficient}]"
