from optparse import make_option, OptionParser
from django.core.management.base import (BaseCommand, CommandError)
from django.db.models import Max
from datetime import timedelta, datetime
from django.conf import settings
from CdrAnalytics.cdr.models import CallDetailRecord, CallStatus

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
        make_option('--interval',
            dest='interval',
            default='0',
            help="Time interval between indexing call status counts in seconds."),
        make_option('--destroy',
            dest='destroy',
            default="False",
            help="Destroy already indexed call status data and start fresh.")
        )

    def handle(self, *args, **options):
        if options.get('destroy').lower() == 'true':
            CallStatus.objects.all().delete()
        from_time_str = options.get('from', '').strip() or None
        to_time_str = options.get('to', '').strip() or None
        interval = int(options.get('interval', '0')) or settings.CALL_STATS_CALC_PERIOD
        time_delta = timedelta(seconds=interval)
        if from_time_str:
            lb = datetime.strptime(from_time_str, '%m/%d/%Y %H')
        else:
            last_index = CallStatus.objects.aggregate(max=Max('time'))['max']
            if last_index:
                last_index += time_delta
            lb =  last_index or datetime.strptime(
                        '9/1/2012', '%m/%d/%Y')
        if to_time_str:
            ub = datetime.strptime(to_time_str, '%m/%d/%Y %H')
        else:
            ub = datetime.now()
        print "Indexing call status counts from %s to %s" % (lb, ub)
        CallDetailRecord.objects.index_call_stats(lb, ub, interval=interval)
