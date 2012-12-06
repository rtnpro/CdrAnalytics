from django.db import models
from django.utils.translation import ugettext_lazy as _
from timedelta.fields import TimedeltaField


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
            verbose_name=_("Call status"))
    start = models.DateTimeField(verbose_name=_("Call start time"))
    duration = TimedeltaField(
            verbose_name=_("Duration of call"))

    def __unicode__(self):
        return "%s -> %s, status:%s, time: %s, dur: %s" % (
                self.from_number, self.to_number, self.status,
                self.start, self.duration)

    @property
    def finish(self):
        return self.start + duration