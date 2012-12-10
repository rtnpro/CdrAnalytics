A django app to generate analytics for call detail records.

Setup instructions
------------------
1. ``git clone https://github.com/rtnpro/CdrAnalytics.git``
1. ``cd CdrAnalytics``
1. ``pip install -r requirements.txt``
1. ``cd CdrAnalytics; cp settings/local.py.dist settings/local.py``
   Configure database settings in ``settings/local.py``. Add corresponding db in postgres.
   ``cd ..``
1. ``./manage.py collectstatic -l``
1. ``./manage.py initialize_cdrs``
1. ``./manage.py max_call_count_stats``
1. ``./manage.py runserver``
1. Visit ``http://127.0.0.1:8000``, enter ``from`` and ``to`` dates in MM/DD/YYYY format to see max call counts per hour stats.
