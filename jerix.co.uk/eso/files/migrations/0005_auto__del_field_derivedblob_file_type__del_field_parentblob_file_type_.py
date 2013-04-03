# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'DerivedDocument', fields ['index', 'derived_from']
        db.delete_unique(u'files_deriveddocument', ['index', 'derived_from_id'])

        # Deleting field 'DerivedBlob.file_type'
        db.delete_column(u'files_derivedblob', 'file_type')

        # Deleting field 'ParentBlob.file_type'
        db.delete_column(u'files_parentblob', 'file_type')

        # Adding unique constraint on 'DerivedDocument', fields ['file_type', 'index', 'derived_from']
        db.create_unique(u'files_deriveddocument', ['file_type', 'index', 'derived_from_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'DerivedDocument', fields ['file_type', 'index', 'derived_from']
        db.delete_unique(u'files_deriveddocument', ['file_type', 'index', 'derived_from_id'])

        # Adding field 'DerivedBlob.file_type'
        db.add_column(u'files_derivedblob', 'file_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding field 'ParentBlob.file_type'
        db.add_column(u'files_parentblob', 'file_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30),
                      keep_default=False)

        # Adding unique constraint on 'DerivedDocument', fields ['index', 'derived_from']
        db.create_unique(u'files_deriveddocument', ['index', 'derived_from_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'files.derivedblob': {
            'Meta': {'unique_together': "(('upload_to_url', 'md5_sum'),)", 'object_name': 'DerivedBlob'},
            'extracted_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extraction_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_sum': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'upload_to_url': ('django.db.models.fields.CharField', [], {'default': "'UnknownDerivedBlobs/'", 'max_length': '100'})
        },
        u'files.deriveddocument': {
            'Meta': {'ordering': "['derived_from', 'index']", 'unique_together': "(('index', 'derived_from', 'file_type'),)", 'object_name': 'DerivedDocument'},
            '_blob': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['files.DerivedBlob']"}),
            'derived_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'derived_documents'", 'to': u"orm['files.ParentBlob']"}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'files.document': {
            'Meta': {'object_name': 'Document'},
            '_blob': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['files.ParentBlob']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'files.parentblob': {
            'Meta': {'object_name': 'ParentBlob'},
            'extracted_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extraction_error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_sum': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['files']
