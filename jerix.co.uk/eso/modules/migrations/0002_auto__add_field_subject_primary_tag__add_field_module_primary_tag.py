# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Subject.primary_tag'
        db.add_column(u'modules_subject', 'primary_tag',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='+', to=orm['taggit.Tag']),
                      keep_default=False)

        # Adding field 'Module.primary_tag'
        db.add_column(u'modules_module', 'primary_tag',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='+', to=orm['taggit.Tag']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Subject.primary_tag'
        db.delete_column(u'modules_subject', 'primary_tag_id')

        # Deleting field 'Module.primary_tag'
        db.delete_column(u'modules_module', 'primary_tag_id')


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
        u'files.document': {
            'Meta': {'object_name': 'Document'},
            '_blob': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': u"orm['files.ParentBlob']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'files.parentblob': {
            'Meta': {'object_name': 'ParentBlob'},
            'extracted_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5_sum': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        u'modules.academicyear': {
            'Meta': {'object_name': 'AcademicYear'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'modules.history': {
            'Meta': {'ordering': "['-end_date', 'start_date']", 'object_name': 'History'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 9, 10, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'modules.material': {
            'Meta': {'ordering': "['index']", 'unique_together': "(('index', 'post'),)", 'object_name': 'Material'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['files.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'materials'", 'to': u"orm['modules.Post']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'modules.module': {
            'Meta': {'object_name': 'Module'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['taggit.Tag']"}),
            'short_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['modules.Subject']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['modules.AcademicYear']"})
        },
        u'modules.parentpost': {
            'Meta': {'ordering': "['module', 'index']", 'unique_together': "(('module', 'index', 'historical_period'),)", 'object_name': 'ParentPost', '_ormbases': [u'modules.Post']},
            'historical_period': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['modules.History']", 'null': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': u"orm['modules.Module']"}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['modules.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'modules.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'modules.subject': {
            'Meta': {'object_name': 'Subject'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['taggit.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'modules.subpost': {
            'Meta': {'ordering': "['parent', 'index']", 'unique_together': "(('parent', 'index'),)", 'object_name': 'SubPost', '_ormbases': [u'modules.Post']},
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_posts'", 'to': u"orm['modules.ParentPost']"}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['modules.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['modules']