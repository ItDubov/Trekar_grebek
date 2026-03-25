from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Habit(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    frequency = models.IntegerField(default=1)
    reward = models.CharField(max_length=255, null=True, blank=True)
    execution_time = models.IntegerField()
    is_public = models.BooleanField(default=False)
    period_days = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    last_executed = models.DateField(null=True, blank=True)

    def clean(self):
        if self.execution_time > 120:
            raise ValidationError("Время выполнения привычки не может быть больше 120 секунд.")
        if self.reward and self.related_habit:
            raise ValidationError("Можно указать только награду или связанную привычку, не оба поля одновременно.")
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть награды или связанной привычки.")
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

    def time_to_remind(self):
        now = timezone.now()
        habit_time = now.replace(
            hour=self.time.hour,
            minute=self.time.minute,
            second=0,
            microsecond=0
        )
        if abs((habit_time - now).total_seconds()) > 300:
            return False
        if self.last_executed:
            days_since = (now.date() - self.last_executed).days
            if days_since < self.period_days:
                return False
        return True

    def __str__(self):
        return self.action
