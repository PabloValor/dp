# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.open_predictions'
        db.add_column(u'games_game', 'open_predictions',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.open_predictions'
        db.delete_column(u'games_game', 'open_predictions')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'games.fixtureplayerpoints': {
            'Meta': {'object_name': 'FixturePlayerPoints'},
            'fixture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Fixture']"}),
            'gameplayer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['games.GamePlayer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {})
        },
        u'games.game': {
            'Meta': {'object_name': 'Game'},
            'classic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'open_predictions': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner_games'", 'to': u"orm['games.Player']"}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'games'", 'symmetrical': 'False', 'through': u"orm['games.GamePlayer']", 'to': u"orm['games.Player']"}),
            'points_classic': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'points_double': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'points_exact': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'}),
            'points_general': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Tournament']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'games.gameplayer': {
            'Meta': {'object_name': 'GamePlayer'},
            'another_chance': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['games.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initial_points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['games.Player']"}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'games.player': {
            'Meta': {'object_name': 'Player'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'friends': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['games.Player']", 'through': u"orm['games.PlayerFriend']", 'symmetrical': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'games.playerfriend': {
            'Meta': {'object_name': 'PlayerFriend'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friend'", 'to': u"orm['games.Player']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friend_player'", 'to': u"orm['games.Player']"}),
            'status': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'games.playermatchprediction': {
            'Meta': {'object_name': 'PlayerMatchPrediction'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gameplayer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_predictions'", 'to': u"orm['games.GamePlayer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_double': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'local_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournaments.Match']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visitor_team_goals': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'tournaments.fixture': {
            'Meta': {'ordering': "['number']", 'object_name': 'Fixture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'open_until': ('django.db.models.fields.DateTimeField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fixtures'", 'to': u"orm['tournaments.Tournament']"})
        },
        u'tournaments.match': {
            'Meta': {'object_name': 'Match'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 24, 0, 0)'}),
            'fixture': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': u"orm['tournaments.Fixture']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_classic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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

    complete_apps = ['games']