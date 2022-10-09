from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    class MessageStatuses(models.TextChoices):
        REVIEW = 'r', _('review')
        BLOCKED = 'b', _('blocked')
        CORRECT = 'c', _('correct')

    user_id = models.IntegerField(verbose_name="User id")
    message = models.TextField(verbose_name='Текст')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, null=True, choices=MessageStatuses.choices, default=MessageStatuses.REVIEW)

    def __str__(self):
        return self.message
