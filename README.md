A django app to generate analytics for call detail records.

Setup instructions
------------------
1. ``git clone https://github.com/rtnpro/CdrAnalytics.git``
1. ``cd CdrAnalytics``
1. ``pip install -r requirements.txt``
1. ``cd CdrAnalytics; cp settings/local.py.dist settings/local.py``
   Configure database settings in ``settings/local.py``. Add corresponding db in postgres and optimize settings.
   ``cd ..``
1. ``./manage.py syncdb``
1. ``./manage.py migrate``
1. ``./manage.py collectstatic -l``
1. ``./manage.py initialize_cdrs`` to generate 20 million randon call detail records.
1. ``./manage.py index_max_con_calls`` to index or preprocess hourly maximum concurrent calls count necessary to generate analytics.
1. ``./manage.py index_call_stats`` to index counts of call status to generate analytics.
1. ``./manage.py runserver``
1. Visit ``http://127.0.0.1:8000`` and have fun :)
