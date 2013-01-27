# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Year.short_code'
        db.add_column('students_year', 'short_code',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Year.short_code'
        db.delete_column('students_year', 'short_code')


    models = {
        'students.year': {
            'Meta': {'object_name': 'Year'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['students']