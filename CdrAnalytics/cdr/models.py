from datetime import datetime, timedelta
from django.db import models
from djangobulk.bulk import insert_many, update_many
from django.utils.translation import ugettext_lazy as _
from timedelta.fields import TimedeltaField
from django.db.models import F
from django.db.models import Max, Min


class CallDetailRecordManager(models.Manager):

    def insert_many(self, records):
        insert_many(CallDetailRecord, records)

    def update_many(self, records):
        update_many(CallDetailRecord, records)

    def concurrent_calls_count_at_time(self, t):
        return self.filter(start__gte=t - F('duration'), start__lt=t).count()

    def get_max_concurrent_calls_for_an_hour(self, h):
        lb = h - timedelta(hours=1)
        return max([self.concurrent_calls_count_at_time(t)
            for t in set([lb] + [
                    i[0] for i in self.filter(
                    start__gt=lb, start__lt=h
                    ).distinct('start').values_list('start')
                ]
            )
        ])


class CallDetailRecord(models.Model):
    from_number = models.CharField(max_length=12,
            verbose_name=_("From number"))
    to_number = models.CharField(max_length=12,
            verbose_name=_("To number"))
    STATUS_CHOICES = (
            ("AN", "Answered"),
            ("NA", "Not answered"),
            ("NR", "No ring"),
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES,
            verbose_name=_("Call status"), db_index=True)
    start = models.DateTimeField(verbose_name=_("Call start time"),
        db_index=True)
    duration = TimedeltaField(
            verbose_name=_("Duration of call"))

    objects = CallDetailRecordManager()

    def __unicode__(self):
        return "%s -> %s, status:%s, time: %s, dur: %s" % (
                self.from_number, self.to_number, self.status,
                self.start, self.duration)

    @property
    def finish(self):
        return self.start + duration


def to_roof(t, always=False):
    if t.minute or always:
        t += timedelta(hours=1)
    t = t.strptime(t.strftime('%m/%d/%Y %H'), '%m/%d/%Y %H')
    return t


def index_max_con_call_count_per_hour():
    lb = to_roof(MaxConCallCountPerHour.objects.aggregate(lb=Max('hour'))['lb'] or \
            CallDetailRecord.objects.aggregate(lb=Min('start'))['lb'], True)
    ub = to_roof(CallDetailRecord.objects.aggregate(ub=Max('start'))['ub'])
    while lb <= ub:
        max_count = CallDetailRecord.objects.get_max_concurrent_calls_for_an_hour(lb)
        MaxConCallCountPerHour.objects.create(hour=lb, max_con_count=max_count)
        lb += timedelta(hours=1)


class MaxConCallCountPerHour(models.Model):
    hour = models.DateTimeField(db_index=True)
    max_con_count = models.IntegerField()

    def __unicode__(self):
        return "hour: %s max_con_calls: %s" % (self.hour, self.max_con_count)