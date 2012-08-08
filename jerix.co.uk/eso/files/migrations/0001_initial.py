# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ParentBlob'
        db.create_table('files_parentblob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('extracted_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('md5_sum', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal('files', ['ParentBlob'])

        # Adding model 'DerivedBlob'
        db.create_table('files_derivedblob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('extracted_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('upload_to_url', self.gf('django.db.models.fields.CharField')(default='UnknownDerivedBlobs:', max_length=100)),
            ('md5_sum', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('files', ['DerivedBlob'])

        # Adding unique constraint on 'DerivedBlob', fields ['upload_to_url', 'md5_sum']
        db.create_unique('files_derivedblob', ['upload_to_url', 'md5_sum'])

        # Adding model 'Document'
        db.create_table('files_document', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('_blob', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documents', to=orm['files.ParentBlob'])),
        ))
        db.send_create_signal('files', ['Document'])

        # Adding model 'DerivedDocument'
        db.create_table('files_deriveddocument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_blob', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documents', to=orm['files.DerivedBlob'])),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('derived_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='derived_documents', to=orm['files.ParentBlob'])),
        ))
        db.send_create_signal('files', ['DerivedDocument'])

        # Adding unique constraint on 'DerivedDocument', fields ['index', 'derived_from']
        db.create_unique('files_deriveddocument', ['index', 'derived_from_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'DerivedDocument', fields ['index', 'derived_from']
        db.delete_unique('files_deriveddocument', ['index', 'derived_from_id'])

        # Removing unique constraint on 'DerivedBlob', fields ['upload_to_url', 'md5_sum']
        db.delete_unique('files_derivedblob', ['upload_to_url', 'md5_sum'])

        # Deleting model 'ParentBlob'
        db.delete_table('files_parentblob')

        # Deleting model 'DerivedBlob'
        db.delete_table('files_derivedblob')

        # Deleting model 'Document'
        db.delete_table('files_document')

        # Deleting model 'DerivedDocument'
        db.delete_table('files_deriveddocument')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'files.derivedblob': {
            'Meta': {'unique_together': "(('upload_to_url', 'md5_sum'),)", 'object_name': 'DerivedBlob'},
            'extracted_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_sum': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'upload_to_url': ('django.db.models.fields.CharField', [], {'default': "'UnknownDerivedBlobs:'", 'max_length': '100'})
        },
        'files.deriveddocument': {
            'Meta': {'ordering': "['derived_from', 'index']", 'unique_together': "(('index', 'derived_from'),)", 'object_name': 'DerivedDocument'},
            '_blob': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': "orm['files.DerivedBlob']"}),
            'derived_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'derived_documents'", 'to': "orm['files.ParentBlob']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'files.document': {
            'Meta': {'object_name': 'Document'},
            '_blob': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': "orm['files.ParentBlob']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'files.parentblob': {
            'Meta': {'object_name': 'ParentBlob'},
            'extracted_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_sum': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['files']