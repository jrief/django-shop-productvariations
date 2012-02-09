# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'OptionGroup'
        db.create_table('shop_optiongroups_optiongroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('shop_optiongroups', ['OptionGroup'])

        # Adding model 'Option'
        db.create_table('shop_optiongroups_option', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=12, decimal_places=2)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop_optiongroups.OptionGroup'])),
        ))
        db.send_create_signal('shop_optiongroups', ['Option'])


    def backwards(self, orm):
        
        # Deleting model 'OptionGroup'
        db.delete_table('shop_optiongroups_optiongroup')

        # Deleting model 'Option'
        db.delete_table('shop_optiongroups_option')


    models = {
        'shop_optiongroups.option': {
            'Meta': {'object_name': 'Option'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_optiongroups.OptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'})
        },
        'shop_optiongroups.optiongroup': {
            'Meta': {'object_name': 'OptionGroup'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['shop_optiongroups']
