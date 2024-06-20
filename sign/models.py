from django.db import models


class Sign(models.Model):
    label = models.CharField(max_length=255)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    training = models.ForeignKey('education.Training', on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, related_name='sign_event', null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    signed = models.BooleanField(default=False)
