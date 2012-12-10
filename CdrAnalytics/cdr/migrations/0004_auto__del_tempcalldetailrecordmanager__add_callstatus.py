# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TempCallDetailRecordManager'
        db.delete_table('cdr_tempcalldetailrecordmanager')

        # Adding model 'CallStatus'
        db.create_table('cdr_callstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('status_na', self.gf('django.db.models.fields.IntegerField')()),
            ('status_nr', self.gf('django.db.models.fields.IntegerField')()),
            ('status_an', self.gf('django.db.models.fields.IntegerField')()),
            ('existing_status_na', self.gf('django.db.models.fields.IntegerField')()),
            ('existing_status_nr', self.gf('django.db.models.fields.IntegerField')()),
            ('existing_status_an', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('cdr', ['CallStatus'])


    def backwards(self, orm):
        # Adding model 'TempCallDetailRecordManager'
        db.create_table('cdr_tempcalldetailrecordmanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cdr', ['TempCallDetailRecordManager'])

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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status_an': ('django.db.models.fields.IntegerField', [], {}),
            'status_na': ('django.db.models.fields.IntegerField', [], {}),
            'status_nr': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'cdr.maxconcallcountperhour': {
            'Meta': {'object_name': 'MaxConCallCountPerHour'},
            'hour': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_con_count': ('django.db.models.fields.IntegerField', [], {})
        },
        'cdr.tempcalldetailrecord': {
            'Meta': {'object_name': 'TempCallDetailRecord'},
            'end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['cdr']