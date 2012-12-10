from django.core.management.base import (BaseCommand, CommandError)
from django.db.models import Max
from datetime import timedelta, datetime
from CdrAnalytics.cdr.models import MaxConCallCountPerHour, index_max_con_call_count_per_hour

class Command(BaseCommand):
    help = "Index max concurrent calls count stats"

    def handle(self, *args, **options):
        d1 = MaxConCallCountPerHour.objects.aggregate(max=Max('hour'))['max'] + timedelta(hours=1)
        d2 = datetime.strptime('10/1/2012', '%m/%d/%Y') - timedelta(hours=1)
        print "Indexing max concurrent call count stats from %s to %s" % (d1, d2)
        index_max_con_call_count_per_hour(d1, d2)
