from django.db import models


class Grade(models.Model):
    name = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="grade_user", null=True, blank=True)
    event = models.ForeignKey("event.Event", on_delete=models.CASCADE, related_name="grade_event")
    student = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="grade_training")
    coefficient = models.IntegerField(blank=True, default=1)
    value = models.FloatField()

