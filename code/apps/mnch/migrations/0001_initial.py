# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeologicalCategory'
        db.create_table(u'mnch_geologicalcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalcategory_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalcategory_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'mnch', ['GeologicalCategory'])

        # Adding model 'GeologicalSite'
        db.create_table(u'mnch_geologicalsite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsite_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsite_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mnch.GeologicalCategory'], null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('ckeditor.fields.HTMLField')()),
        ))
        db.send_create_signal(u'mnch', ['GeologicalSite'])

        # Adding model 'GeologicalSitePhoto'
        db.create_table(u'mnch_geologicalsitephoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsitephoto_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsitephoto_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='approved', max_length=32)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mnch.GeologicalSite'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('credits', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=99)),
        ))
        db.send_create_signal(u'mnch', ['GeologicalSitePhoto'])

        # Adding model 'GeologicalSiteResource'
        db.create_table(u'mnch_geologicalsiteresource', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsiteresource_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsiteresource_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mnch.GeologicalSite'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=99)),
        ))
        db.send_create_signal(u'mnch', ['GeologicalSiteResource'])

        # Adding model 'GeologicalSiteComment'
        db.create_table(u'mnch_geologicalsitecomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsitecomment_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='geologicalsitecomment_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='approved', max_length=32)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mnch.GeologicalSite'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('num_likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'mnch', ['GeologicalSiteComment'])

        # Adding model 'Venue'
        db.create_table(u'mnch_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='venue_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='venue_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'mnch', ['Venue'])

        # Adding model 'VolunteerCategory'
        db.create_table(u'mnch_volunteercategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='volunteercategory_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='volunteercategory_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'mnch', ['VolunteerCategory'])

        # Adding model 'VolunteerOpportunity'
        db.create_table(u'mnch_volunteeropportunity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='volunteeropportunity_created', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='volunteeropportunity_updated', null=True, on_delete=models.SET_NULL, to=orm['auth.User'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mnch.VolunteerCategory'], null=True, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mnch.Venue'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('description', self.gf('ckeditor.fields.HTMLField')(blank=True)),
        ))
        db.send_create_signal(u'mnch', ['VolunteerOpportunity'])


    def backwards(self, orm):
        # Deleting model 'GeologicalCategory'
        db.delete_table(u'mnch_geologicalcategory')

        # Deleting model 'GeologicalSite'
        db.delete_table(u'mnch_geologicalsite')

        # Deleting model 'GeologicalSitePhoto'
        db.delete_table(u'mnch_geologicalsitephoto')

        # Deleting model 'GeologicalSiteResource'
        db.delete_table(u'mnch_geologicalsiteresource')

        # Deleting model 'GeologicalSiteComment'
        db.delete_table(u'mnch_geologicalsitecomment')

        # Deleting model 'Venue'
        db.delete_table(u'mnch_venue')

        # Deleting model 'VolunteerCategory'
        db.delete_table(u'mnch_volunteercategory')

        # Deleting model 'VolunteerOpportunity'
        db.delete_table(u'mnch_volunteeropportunity')


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
        u'mnch.geologicalcategory': {
            'Meta': {'object_name': 'GeologicalCategory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalcategory_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalcategory_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mnch.geologicalsite': {
            'Meta': {'object_name': 'GeologicalSite'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mnch.GeologicalCategory']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsite_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'description': ('ckeditor.fields.HTMLField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsite_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mnch.geologicalsitecomment': {
            'Meta': {'ordering': "('-created_at',)", 'object_name': 'GeologicalSiteComment'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsitecomment_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mnch.GeologicalSite']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'approved'", 'max_length': '32'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsitecomment_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mnch.geologicalsitephoto': {
            'Meta': {'ordering': "('position', 'name')", 'object_name': 'GeologicalSitePhoto'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsitephoto_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '99'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mnch.GeologicalSite']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'approved'", 'max_length': '32'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsitephoto_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mnch.geologicalsiteresource': {
            'Meta': {'ordering': "('position', 'name')", 'object_name': 'GeologicalSiteResource'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsiteresource_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '99'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mnch.GeologicalSite']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'geologicalsiteresource_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'mnch.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'venue_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'venue_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'mnch.volunteercategory': {
            'Meta': {'object_name': 'VolunteerCategory'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'volunteercategory_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'volunteercategory_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"})
        },
        u'mnch.volunteeropportunity': {
            'Meta': {'object_name': 'VolunteerOpportunity'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mnch.VolunteerCategory']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'volunteeropportunity_created'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('ckeditor.fields.HTMLField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'volunteeropportunity_updated'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mnch.Venue']"})
        }
    }

    complete_apps = ['mnch']