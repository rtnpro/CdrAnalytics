# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PrefixNumbers'
        db.create_table('cdr_prefixnumbers', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefix', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('cdr', ['PrefixNumbers'])


    def backwards(self, orm):
        # Deleting model 'PrefixNumbers'
        db.delete_table('cdr_prefixnumbers')


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
        'cdr.callstatus': {
            'Meta': {'object_name': 'CallStatus'},
            'existing_status_an': ('django.db.models.fields.IntegerField', [], {}),
            'existing_status_na': ('django.db.models.fields.IntegerField', [], {}),
            'existing_status_nr': ('django.db.models.fields.IntegerField', [], {}),
            'status_an': ('django.db.models.fields.IntegerField', [], {}),
            'status_na': ('django.db.models.fields.IntegerField', [], {}),
            'status_nr': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'primary_key': 'True', 'db_index': 'True'})
        },
        'cdr.maxconcallcountperhour': {
            'Meta': {'object_name': 'MaxConCallCountPerHour'},
            'hour': ('django.db.models.fields.DateTimeField', [], {'primary_key': 'True', 'db_index': 'True'}),
            'max_con_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'cdr.prefixnumbers': {
            'Meta': {'object_name': 'PrefixNumbers'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prefix': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['cdr']