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
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('duration', self.gf('timedelta.fields.TimedeltaField')()),
        ))
        db.send_create_signal('cdr', ['CallDetailRecord'])

        # Adding model 'MaxConCallCountPerHour'
        db.create_table('cdr_maxconcallcountperhour', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hour', self.gf('django.db.models.fields.DateTimeField')()),
            ('max_con_count', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cdr', ['MaxConCallCountPerHour'])


    def backwards(self, orm):
        # Deleting model 'CallDetailRecord'
        db.delete_table('cdr_calldetailrecord')

        # Deleting model 'MaxConCallCountPerHour'
        db.delete_table('cdr_maxconcallcountperhour')


    models = {
        'cdr.calldetailrecord': {
            'Meta': {'object_name': 'CallDetailRecord'},
            'duration': ('timedelta.fields.TimedeltaField', [], {}),
            'from_number': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'to_number': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'cdr.maxconcallcountperhour': {
            'Meta': {'object_name': 'MaxConCallCountPerHour'},
            'hour': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_con_count': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['cdr']