from optparse import make_option, OptionParser
import os.path
import sys
from django.core.management.base import (BaseCommand, CommandError)
from django.db.models import get_model
from django.conf import settings

import random
from datetime import timedelta, datetime

START_TIME = '9/1/2012'
END_TIME = '10/1/2012'
DATE_FORMAT = '%m/%d/%Y'
PHONE_LOWER_LIMIT = 8 * 10**11
PHONE_UPPER_LIMIT = int(9.9 * 10 ** 11)


CallDetailRecord = get_model('cdr', 'CallDetailRecord')


def random_datetime(start=datetime.strptime(START_TIME, DATE_FORMAT),
        end=datetime.strptime(END_TIME, DATE_FORMAT)):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return (start + timedelta(seconds=random_second))


def get_rand_ph_numbers():
    return str(random.randrange(PHONE_LOWER_LIMIT, PHONE_UPPER_LIMIT)), \
            str(random.randrange(PHONE_LOWER_LIMIT, PHONE_UPPER_LIMIT))


def generate_random_cdr(start, end):
    from_no, to_no = get_rand_ph_numbers()
    status = random.choice(['AN', 'NA', 'NR'])
    start_time = random_datetime()
    duration = timedelta(seconds=random.randrange(1, 7201))
    return CallDetailRecord(from_number=from_no, to_number=to_no,
            status=status, start=start_time,
            duration=duration)

def generate_n_cdrs(n, start, end):
    count = 0
    l = []
    seg_size = 1000
    seg_count=0
    for i in range(n):
        if seg_count == seg_size:
            print "Writing records to db..."
            CallDetailRecord.objects.bulk_create(l)
            l = []
            seg_count = 0
        l.append(generate_random_cdr(start, end))
        count += 1
        seg_count += 1
        print count
    CallDetailRecord.objects.bulk_create(l)


class Command(BaseCommand):
    args = ""
    help = "Initialize 20 million CDRs from 9/1/2012 to 10/1/2012"
    option_list = BaseCommand.option_list + (
        make_option('--from',
            dest='from',
            default='9/1/2012',
            help='Date from which to start generating data.'),
            make_option('--to',
            dest='to',
            default='10/1/2012',
            help='Date upto which data will be generated'),
        make_option('--n',
            dest='n',
            default=20 * 10 ** 6,
            help="Number of CDRs to generate")
        )
    def handle(self, *args, **options):
        n = int(options.get('n', '1'))
        to_date = datetime.strptime(options.get('to'), DATE_FORMAT)
        from_date = datetime.strptime(options.get('from'), DATE_FORMAT)
        generate_n_cdrs(n, from_date, to_date)

