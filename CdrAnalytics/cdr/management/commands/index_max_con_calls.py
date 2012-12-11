from optparse import make_option, OptionParser
from django.core.management.base import (BaseCommand, CommandError)
from django.db.models import Max
from datetime import timedelta, datetime
from CdrAnalytics.cdr.models import MaxConCallCountPerHour, CallDetailRecord

class Command(BaseCommand):
    help = "Index max concurrent calls count stats"
    option_list = BaseCommand.option_list + (
        make_option('--from',
            dest='from',
            default='',
            help='Time from which to index call status counts "MM/DD/YYYY HH" format.'),
        make_option('--to',
            dest='to',
            default='',
            help='Time upto which to index call status counts in "MM/DD/YYYY HH" format.'),
        make_option('--destroy',
            dest='destroy',
            default="False",
            help="Destroy already indexed maximum hourly concurrent calls "
                 "data and start fresh.")
        )

    def handle(self, *args, **options):
        if options.get('destroy').lower == 'true':
            MaxConCallCountPerHour.objects.all().delete()
        from_time_str = options.get('from', '').strip() or None
        to_time_str = options.get('to', '').strip() or None
        if from_time_str:
            lb = datetime.strptime(from_time_str, '%m/%d/%Y %H')
        else:
            last_indexed_hour = MaxConCallCountPerHour.objects.aggregate(
                    max=Max('hour'))['max']
            lb = last_indexed_hour + timedelta(hours=1) if last_indexed_hour else \
                        datetime.strptime('9/1/2012', '%m/%d/%Y')
        if to_time_str:
            ub = datetime.strptime(to_time_str, '%m/%d/%Y %H')
        else:
            ub = datetime.strptime('10/1/2012', '%m/%d/%Y') - timedelta(hours=1)
        print "Indexing max concurrent call count stats from %s to %s" % (lb, ub)
        CallDetailRecord.objects.index_max_con_call_counts(lb, ub)
