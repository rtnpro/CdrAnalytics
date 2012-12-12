from datetime import datetime, timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _
from timedelta.fields import TimedeltaField
from django.db.models import F, Q, Max, Min, Count, Sum
from django.conf import settings


def to_roof(t, always=False):
    if t.minute or always:
        t += timedelta(hours=1)
    t = t.strptime(t.strftime('%m/%d/%Y %H'), '%m/%d/%Y %H')
    return t


class CallDetailRecordManager(models.Manager):

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

    def index_call_stats_for_time_t(self, t, delta=timedelta(hours=1)):
        d = datetime.now()
        q = CallStatus.objects.filter(time=t)
        call_status = q and q[0] or \
                CallStatus(time=t)
        default_call_status_attrs = {
                    'status_na': 0, 'status_an': 0,
                    'status_nr': 0, 'existing_status_na': 0,
                    'existing_status_nr': 0, 'existing_status_an': 0
                    }
        call_status, created = CallStatus.objects.get_or_create(
                time=t, defaults=default_call_status_attrs
                )
        if not created:
            [setattr(call_status, attr, value)
                    for attr, value in default_call_status_attrs.items()]
        q = CallDetailRecord.objects.filter(start__gte=t, start__lt=t + delta).values('status')
        for cdr in q.iterator():
            if cdr.get('status') == 'NA':
                call_status.status_na += 1
            elif cdr.get('status') == 'AN':
                call_status.status_an += 1
            elif cdr.get('status') == 'NR':
                call_status.status_nr += 1
        q = CallDetailRecord.objects.filter(start__lt=t, start__gt=t - F('duration')).values(
                'status')
        for cdr in q.iterator():
            if cdr.get('status') == 'NA':
                call_status.existing_status_na += 1
            elif cdr.get('status') == 'AN':
                call_status.existing_status_an += 1
            elif cdr.get('status') == 'NR':
                call_status.existing_status_nr += 1
        call_status.save()
        print "Calculated call status for time %s in %d seconds: %s" % (
                t, (datetime.now() - d).seconds, call_status)

    def index_call_stats(self, lb, ub, interval=None):
        delta = timedelta(seconds=interval or settings.CALL_STATS_CALC_PERIOD)
        t = lb
        while t < ub:
            self.index_call_stats_for_time_t(t, delta=delta)
            t += delta

    def get_status_counts(self, lb, ub):
        qs = CallStatus.objects.filter(
                time__gte=lb, time__lt=ub).order_by('time')
        status_count_dict = qs.aggregate(
                na=Sum('status_na'), an=Sum('status_an'), nr=Sum('status_nr'))
        existing_status_count_dict = {}
        if qs:
            cs0 = qs[0]
            existing_status_count_dict = {
                    'na': cs0.existing_status_na,
                    'an': cs0.existing_status_an,
                    'nr': cs0.existing_status_nr
                }
        return [
            {
                'type': 'Not answered',
                'count': existing_status_count_dict.get('na', 0) + \
                    (status_count_dict.get('na') or 0)
            },
            {
                'type': 'Answered',
                'count': existing_status_count_dict.get('an', 0) + \
                    (status_count_dict.get('an') or 0)
            },
            {
                'type': 'No ring',
                'count': existing_status_count_dict.get('nr', 0) + \
                    (status_count_dict.get('nr') or 0)
            }
        ]

    def index_max_con_call_counts(self, lb=None, ub=None):
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
            max_count = self.get_max_concurrent_calls_for_an_hour(lb)
            m, created = MaxConCallCountPerHour.objects.get_or_create(
                    hour=lb, defaults={'max_con_count':max_count})
            if not created:
                m.max_con_count = max_count
                m.save()
            print "Calculated max concurrent call count for %s in %d seconds: %d" % (
                    lb, (datetime.now() - d).seconds, max_count)
            lb += timedelta(hours=1)


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


class MaxConCallCountPerHour(models.Model):
    hour = models.DateTimeField(db_index=True, primary_key=True)
    max_con_count = models.IntegerField()

    def __unicode__(self):
        return "hour: %s max_con_calls: %s" % (self.hour, self.max_con_count)


class CallStatus(models.Model):
    time = models.DateTimeField(db_index=True, primary_key=True)
    # status counts for new calls
    status_na = models.IntegerField()
    status_nr = models.IntegerField()
    status_an = models.IntegerField()
    # status counts for existing calls
    existing_status_na = models.IntegerField()
    existing_status_nr = models.IntegerField()
    existing_status_an = models.IntegerField()

    def __unicode__(self):
        return "%s, NA: %d, AN: %d, NR: %d" % (
                self.time, self.status_na, self.status_an,
                self.status_nr
            )
