# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CallDetailRecord'
        db.create_table('cdr_calldetailrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_number', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('to_number', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2, db_index=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('duration', self.gf('timedelta.fields.TimedeltaField')()),
        ))
        db.send_create_signal('cdr', ['CallDetailRecord'])
        db.create_index('cdr_calldetailrecord', ['start', 'duration'])

        # Adding model 'MaxConCallCountPerHour'
        db.create_table('cdr_maxconcallcountperhour', (
            ('hour', self.gf('django.db.models.fields.DateTimeField')(primary_key=True, db_index=True)),
            ('max_con_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cdr', ['MaxConCallCountPerHour'])

        # Adding model 'CallStatus'
        db.create_table('cdr_callstatus', (
            ('time', self.gf('django.db.models.fields.DateTimeField')(primary_key=True, db_index=True)),
            ('status_na', self.gf('django.db.models.fields.IntegerField')()),
            ('status_nr', self.gf('django.db.models.fields.IntegerField')()),
            ('status_an', self.gf('django.db.models.fields.IntegerField')()),
            ('existing_status_na', self.gf('django.db.models.fields.IntegerField')()),
            ('existing_status_nr', self.gf('django.db.models.fields.IntegerField')()),
            ('existing_status_an', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cdr', ['CallStatus'])


    def backwards(self, orm):
        # Deleting model 'CallDetailRecord'
        db.delete_table('cdr_calldetailrecord')

        # Deleting model 'MaxConCallCountPerHour'
        db.delete_table('cdr_maxconcallcountperhour')

        # Deleting model 'CallStatus'
        db.delete_table('cdr_callstatus')


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
        }
    }

    complete_apps = ['cdr']
