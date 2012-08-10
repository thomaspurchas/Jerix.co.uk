# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field lecturers_new on 'Module'
        db.delete_table('modules_module_lecturers_new')


    def backwards(self, orm):
        # Adding M2M table for field lecturers_new on 'Module'
        db.create_table('modules_module_lecturers_new', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module', models.ForeignKey(orm['modules.module'], null=False)),
            ('lecturerprofile', models.ForeignKey(orm['accounts.lecturerprofile'], null=False))
        ))
        db.create_unique('modules_module_lecturers_new', ['module_id', 'lecturerprofile_id'])


    models = {
        'accounts.lecturerprofile': {
            'Meta': {'object_name': 'LecturerProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
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
        },
        'modules.academicyear': {
            'Meta': {'object_name': 'AcademicYear'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'modules.history': {
            'Meta': {'ordering': "['-end_date', 'start_date']", 'object_name': 'History'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 8, 10, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'modules.material': {
            'Meta': {'ordering': "['index']", 'unique_together': "(('index', 'post'),)", 'object_name': 'Material'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['files.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'materials'", 'to': "orm['modules.Post']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'modules.module': {
            'Meta': {'object_name': 'Module'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecturers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'modules'", 'symmetrical': 'False', 'to': "orm['accounts.LecturerProfile']"}),
            'short_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modules.Subject']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modules.AcademicYear']"})
        },
        'modules.parentpost': {
            'Meta': {'ordering': "['module', 'index']", 'unique_together': "(('module', 'index', 'historical_period'),)", 'object_name': 'ParentPost', '_ormbases': ['modules.Post']},
            'historical_period': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['modules.History']", 'null': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['modules.Module']"}),
            'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['modules.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        'modules.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'modules.subject': {
            'Meta': {'object_name': 'Subject'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'modules.subpost': {
            'Meta': {'ordering': "['parent', 'index']", 'unique_together': "(('parent', 'index'),)", 'object_name': 'SubPost', '_ormbases': ['modules.Post']},
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_posts'", 'to': "orm['modules.ParentPost']"}),
            'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['modules.Post']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['modules']