# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntityReputation'
        db.create_table('reputation_entityreputation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('reputation', ['EntityReputation'])

        # Adding M2M table for field up_votes on 'EntityReputation'
        db.create_table('reputation_entityreputation_up_votes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entityreputation', models.ForeignKey(orm['reputation.entityreputation'], null=False)),
            ('userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False))
        ))
        db.create_unique('reputation_entityreputation_up_votes', ['entityreputation_id', 'userprofile_id'])

        # Adding M2M table for field down_votes on 'EntityReputation'
        db.create_table('reputation_entityreputation_down_votes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entityreputation', models.ForeignKey(orm['reputation.entityreputation'], null=False)),
            ('userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False))
        ))
        db.create_unique('reputation_entityreputation_down_votes', ['entityreputation_id', 'userprofile_id'])

        # Adding model 'ReputationReward'
        db.create_table('reputation_reputationreward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('reputation_amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('reputation', ['ReputationReward'])


    def backwards(self, orm):
        # Deleting model 'EntityReputation'
        db.delete_table('reputation_entityreputation')

        # Removing M2M table for field up_votes on 'EntityReputation'
        db.delete_table('reputation_entityreputation_up_votes')

        # Removing M2M table for field down_votes on 'EntityReputation'
        db.delete_table('reputation_entityreputation_down_votes')

        # Deleting model 'ReputationReward'
        db.delete_table('reputation_reputationreward')


    models = {
        'accounts.lecturerprofile': {
            'Meta': {'object_name': 'LecturerProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'accounts.studentprofile': {
            'Meta': {'object_name': 'StudentProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['modules.Module']", 'symmetrical': 'False'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.LecturerProfile']"}),
            'year': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['students.Year']"})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'about_me': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'current_reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecturer_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.LecturerProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'student_profile': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.StudentProfile']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
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
        'modules.academicyear': {
            'Meta': {'object_name': 'AcademicYear'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
        'modules.subject': {
            'Meta': {'object_name': 'Subject'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reputation.entityreputation': {
            'Meta': {'object_name': 'EntityReputation'},
            'down_votes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'votes_down'", 'symmetrical': 'False', 'to': "orm['accounts.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'up_votes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'votes_up'", 'symmetrical': 'False', 'to': "orm['accounts.UserProfile']"})
        },
        'reputation.reputationreward': {
            'Meta': {'object_name': 'ReputationReward'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reputation_amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'students.year': {
            'Meta': {'object_name': 'Year'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['reputation']