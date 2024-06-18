from django.db import models


class Event(models.Model):
    label = models.CharField(max_length=255)
    # owner of the event
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    instructor = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='instructor', null=True, blank=True)
    # classroom = models.ForeignKey('main.Training', on_delete=models.CASCADE, null=True, blank=True)
    type = models.IntegerField(choices=[
        (1, 'personal'),
        (2, 'course'),
    ], default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    full_day = models.BooleanField(default=False)
