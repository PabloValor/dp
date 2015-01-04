# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TournamentHomepage'
        db.create_table(u'homepage_tournamenthomepage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Tournament'])),
        ))
        db.send_create_signal(u'homepage', ['TournamentHomepage'])


    def backwards(self, orm):
        # Deleting model 'TournamentHomepage'
        db.delete_table(u'homepage_tournamenthomepage')


    models = {
        u'homepage.tournamenthomepage': {
            'Meta': {'object_name': 'TournamentHomepage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Tournament']"})
        },
        u'tournaments.tournament': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tournament'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['homepage']