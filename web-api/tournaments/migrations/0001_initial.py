# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tournament'
        db.create_table(u'tournaments_tournament', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'tournaments', ['Tournament'])

        # Adding model 'Team'
        db.create_table(u'tournaments_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('crest', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'tournaments', ['Team'])

        # Adding model 'Fixture'
        db.create_table(u'tournaments_fixture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Tournament'])),
            ('open_until', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'tournaments', ['Fixture'])

        # Adding model 'Match'
        db.create_table(u'tournaments_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 5, 24, 0, 0))),
            ('local_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='local_team', to=orm['tournaments.Team'])),
            ('local_team_goals', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('visitor_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='visitor_team', to=orm['tournaments.Team'])),
            ('visitor_team_goals', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('fixture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournaments.Fixture'])),
            ('suspended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_classic', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tournaments', ['Match'])


    def backwards(self, orm):
        # Deleting model 'Tournament'
        db.delete_table(u'tournaments_tournament')

        # Deleting model 'Team'
        db.delete_table(u'tournaments_team')

        # Deleting model 'Fixture'
        db.delete_table(u'tournaments_fixture')

        # Deleting model 'Match'
        db.delete_table(u'tournaments_match')


    models = {
        u'tournaments.fixture': {
            'Meta': {'ordering': "['number']", 'object_name': 'Fixture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'open_until': ('django.db.models.fields.DateTimeField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Tournament']"})
        },
        u'tournaments.match': {
            'Meta': {'object_name': 'Match'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 5, 24, 0, 0)'}),
            'fixture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Fixture']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_classic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'local_team'", 'to': u"orm['tournaments.Team']"}),
            'local_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visitor_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visitor_team'", 'to': u"orm['tournaments.Team']"}),
            'visitor_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'tournaments.team': {
            'Meta': {'ordering': "['name']", 'object_name': 'Team'},
            'crest': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tournaments.tournament': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tournament'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['tournaments']