# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RSSFeed'
        db.create_table('glean_rssfeed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(related_name='glean_rssfeed_feeds', to=orm['glean.Search'])),
            ('force_term_filter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('max_update_frequency', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('glean', ['RSSFeed'])

        # Adding M2M table for field articles on 'RSSFeed'
        db.create_table('glean_rssfeed_articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rssfeed', models.ForeignKey(orm['glean.rssfeed'], null=False)),
            ('article', models.ForeignKey(orm['glean.article'], null=False))
        ))
        db.create_unique('glean_rssfeed_articles', ['rssfeed_id', 'article_id'])


    def backwards(self, orm):
        
        # Deleting model 'RSSFeed'
        db.delete_table('glean_rssfeed')

        # Removing M2M table for field articles on 'RSSFeed'
        db.delete_table('glean_rssfeed_articles')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 23, 17, 1, 18, 819367)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 1, 23, 17, 1, 18, 819245)'}),
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
        'glean.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extra_meta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'found_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'glean.rssfeed': {
            'Meta': {'object_name': 'RSSFeed'},
            'articles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'glean_rssfeed_sources'", 'symmetrical': 'False', 'to': "orm['glean.Article']"}),
            'force_term_filter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'max_update_frequency': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'glean_rssfeed_feeds'", 'to': "orm['glean.Search']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'glean.search': {
            'Meta': {'object_name': 'Search'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'synonyms': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'glean.snapshot': {
            'Meta': {'object_name': 'Snapshot'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['glean.Article']"}),
            'body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['glean']
