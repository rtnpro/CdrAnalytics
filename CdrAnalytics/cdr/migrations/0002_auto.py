# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'CallDetailRecord', fields ['status']
        db.create_index('cdr_calldetailrecord', ['status'])

        # Adding index on 'CallDetailRecord', fields ['start']
        db.create_index('cdr_calldetailrecord', ['start'])

        # Adding index on 'MaxConCallCountPerHour', fields ['hour']
        db.create_index('cdr_maxconcallcountperhour', ['hour'])


    def backwards(self, orm):
        # Removing index on 'MaxConCallCountPerHour', fields ['hour']
        db.delete_index('cdr_maxconcallcountperhour', ['hour'])

        # Removing index on 'CallDetailRecord', fields ['start']
        db.delete_index('cdr_calldetailrecord', ['start'])

        # Removing index on 'CallDetailRecord', fields ['status']
        db.delete_index('cdr_calldetailrecord', ['status'])


    models = {
        'cdr.calldetailrecord': {
            'Meta': {'object_name': 'CallDetailRecord'},
            'duration': ('timedelta.fields.TimedeltaField', [], {}),
            'from_number': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'to_number': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'cdr.maxconcallcountperhour': {
            'Meta': {'object_name': 'MaxConCallCountPerHour'},
            'hour': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_con_count': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['cdr']