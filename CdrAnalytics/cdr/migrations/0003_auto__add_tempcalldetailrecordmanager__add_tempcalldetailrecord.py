# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TempCallDetailRecordManager'
        db.create_table('cdr_tempcalldetailrecordmanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cdr', ['TempCallDetailRecordManager'])

        # Adding model 'TempCallDetailRecord'
        db.create_table('cdr_tempcalldetailrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal('cdr', ['TempCallDetailRecord'])


    def backwards(self, orm):
        # Deleting model 'TempCallDetailRecordManager'
        db.delete_table('cdr_tempcalldetailrecordmanager')

        # Deleting model 'TempCallDetailRecord'
        db.delete_table('cdr_tempcalldetailrecord')


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
        },
        'cdr.tempcalldetailrecord': {
            'Meta': {'object_name': 'TempCallDetailRecord'},
            'end': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        'cdr.tempcalldetailrecordmanager': {
            'Meta': {'object_name': 'TempCallDetailRecordManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['cdr']