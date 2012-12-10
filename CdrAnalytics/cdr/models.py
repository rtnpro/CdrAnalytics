from datetime import datetime, timedelta
from django.db import models
from djangobulk.bulk import insert_many, update_many
from django.utils.translation import ugettext_lazy as _
from timedelta.fields import TimedeltaField
from django.db.models import F, Q, Max, Min


class TempCallDetailRecord(models.Model):
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)


class CallDetailRecordManager(models.Manager):

    def concurrent_calls_count_at_time(self, t):
        return TempCallDetailRecord.objects.filter(
                end__gte=t, start__lt=t).count()

    def get_max_concurrent_calls_for_an_hour(self, h):
        initial_count = self.filter(start__gt=h - F('duration'),
                start__lt=h).values('id').count()
        start_dict = {}
        end_dict = {}
        cur_count = max_count = initial_count
        for i in self.filter(start__gte=h, start__lt=h + timedelta(hours=1)
                ).values('start').iterator():
            start = i['start']
            if start not in start_dict:
                start_dict[start] = 1
            else:
                start_dict[start] += 1

        for i in self.filter(start__gte=h - F('duration'),
                 start__lt=h + timedelta(hours=1) - F('duration')
                 ).values('start', 'duration').iterator():
            end = i['start'] + i['duration']
            if end not in end_dict:
                end_dict[end] = 1
            else:
                end_dict[end] += 1

        for i in range(3600):
            t = h + timedelta(seconds=i)
            cur_count += start_dict.get(t, 0) - end_dict.get(t, 0)
            if cur_count > max_count:
                max_count = cur_count
        return max_count


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


def index_max_con_call_count_per_hour(lb=None, ub=None):
    if not lb:
        lb = to_roof(MaxConCallCountPerHour.objects.aggregate(
                lb=Max('hour'))['lb'] or \
                CallDetailRecord.objects.aggregate(
                    lb=Min('start')
                )['lb'], True
              )
    if not ub:
        ub = to_roof(
                CallDetailRecord.objects.aggregate(
                    ub=Max('start')
                )['ub']
             )
    while lb <= ub:
        d = datetime.now()
        max_count = CallDetailRecord.objects.get_max_concurrent_calls_for_an_hour(lb)
        m, created = MaxConCallCountPerHour.objects.get_or_create(
                hour=lb, defaults={'max_con_count':max_count})
        if not created:
            m.update(max_con_count=max_count)
        print "Calculated max concurrent call count for %s in %d seconds: %d" % (
                lb, (datetime.now() - d).seconds, max_count)
        lb += timedelta(hours=1)


class MaxConCallCountPerHour(models.Model):
    hour = models.DateTimeField(db_index=True)
    max_con_count = models.IntegerField()

    def __unicode__(self):
        return "hour: %s max_con_calls: %s" % (self.hour, self.max_con_count)
