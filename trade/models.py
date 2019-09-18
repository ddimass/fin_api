from django.db import models
from django.contrib.auth.models import User


class Instrument(models.Model):
    name = models.CharField(max_length=30)
    desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Bar(models.Model):
    time = models.DateTimeField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    tick_volume = models.BigIntegerField(blank=True, null=True)
    spread = models.IntegerField(blank=True, null=True)
    real_volume = models.BigIntegerField(blank=True, null=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.instrument.name + ' - ' + self.time.strftime("%Y-%m-%d %H:%M:%S")
