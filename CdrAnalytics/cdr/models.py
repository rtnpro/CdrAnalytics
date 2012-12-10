from datetime import datetime, timedelta
from django.db import models
from djangobulk.bulk import insert_many, update_many
from django.utils.translation import ugettext_lazy as _
from timedelta.fields import TimedeltaField
from django.db.models import F
from django.db.models import Max, Min
from django.conf import settings


class TempCallDetailRecord(models.Model):
    start = models.DateTimeField(db_index=True)
    end = models.DateTimeField(db_index=True)


class CallDetailRecordManager(models.Manager):

    def concurrent_calls_count_at_time(self, t, collection, count=0, initial=False):
        if initial:
            return collection.find({'end': {'$gt': t},
                'start': {'$lte': t}}).count()
        start_count = collection.find({'start': t}).count()
        end_count = collection.find({'end': t}).count()
        count += start_count - end_count
        return count

    def get_max_concurrent_calls_for_an_hour(self, h):
        from pymongo import Connection
        c = Connection()
        db = getattr(c, settings.MONGO_DB_NAME)
        collection = getattr(db, settings.MONGO_COLLECTION_NAME)

        lb = h - timedelta(hours=1)
        max_count = cur_call_count = self.concurrent_calls_count_at_time(
                lb, collection, initial=True)
        for i in range(3600):
            t = lb + timedelta(seconds=i)
            cur_call_count = self.concurrent_calls_count_at_time(t, collection, count=cur_call_count)
            max_count = cur_call_count if cur_call_count > max_count else max_counta
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
    lb += timedelta(hours=1)
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
        max_count = CallDetailRecord.objects.get_max_concurrent_calls_for_an_hour(lb)
        m, created = MaxConCallCountPerHour.objects.get_or_create(
                hour=lb, defaults={'max_con_count':max_count})
        if not created:
            m.update(max_con_count=max_count)
        lb += timedelta(hours=1)


def insert_cdrs_to_mongo(db, start, to, cdrs=[]):
    print start, to
    count = 0
    collection = db.cdr_collection
    for i in CallDetailRecord.objects.filter(start__gte=start, start__lt=to).values().iterator():
        if count == 500:
            collection.insert(cdrs)
            count = 0
            del cdrs; cdrs = []
        i.update({'end': i['start'] + i['duration']})
        i.pop('duration')
        #print i
        cdrs.append(i)
        count += 1
    if count > 0:
        collection.insert(cdrs)
    del cdrs

def cacherecords(start, end):
    from pymongo import Connection
    connection = Connection()
    db = connection.cdr_analytics
    diff_hours = (end - start).days * 24
    to = start
    for d in range(diff_hours):
        to = start + timedelta(hours=d + 1)
        insert_cdrs_to_mongo(db, to - timedelta(hours=1), to)
    if to < end:
        insert_cdrs_to_mongo(db, to , end)


class MaxConCallCountPerHour(models.Model):
    hour = models.DateTimeField(db_index=True)
    max_con_count = models.IntegerField()

    def __unicode__(self):
        return "hour: %s max_con_calls: %s" % (self.hour, self.max_con_count)
