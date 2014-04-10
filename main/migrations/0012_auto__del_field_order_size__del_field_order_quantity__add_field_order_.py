# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Order.size'
        db.delete_column(u'main_order', 'size')

        # Deleting field 'Order.quantity'
        db.delete_column(u'main_order', 'quantity')

        # Adding field 'Order.qty_1'
        db.add_column(u'main_order', 'qty_1',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_2'
        db.add_column(u'main_order', 'qty_2',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_3'
        db.add_column(u'main_order', 'qty_3',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_4'
        db.add_column(u'main_order', 'qty_4',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_6'
        db.add_column(u'main_order', 'qty_6',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_8'
        db.add_column(u'main_order', 'qty_8',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_10'
        db.add_column(u'main_order', 'qty_10',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_12'
        db.add_column(u'main_order', 'qty_12',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_14'
        db.add_column(u'main_order', 'qty_14',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Order.qty_16'
        db.add_column(u'main_order', 'qty_16',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Order.size'
        db.add_column(u'main_order', 'size',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=2),
                      keep_default=False)

        # Adding field 'Order.quantity'
        db.add_column(u'main_order', 'quantity',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=10),
                      keep_default=False)

        # Deleting field 'Order.qty_1'
        db.delete_column(u'main_order', 'qty_1')

        # Deleting field 'Order.qty_2'
        db.delete_column(u'main_order', 'qty_2')

        # Deleting field 'Order.qty_3'
        db.delete_column(u'main_order', 'qty_3')

        # Deleting field 'Order.qty_4'
        db.delete_column(u'main_order', 'qty_4')

        # Deleting field 'Order.qty_6'
        db.delete_column(u'main_order', 'qty_6')

        # Deleting field 'Order.qty_8'
        db.delete_column(u'main_order', 'qty_8')

        # Deleting field 'Order.qty_10'
        db.delete_column(u'main_order', 'qty_10')

        # Deleting field 'Order.qty_12'
        db.delete_column(u'main_order', 'qty_12')

        # Deleting field 'Order.qty_14'
        db.delete_column(u'main_order', 'qty_14')

        # Deleting field 'Order.qty_16'
        db.delete_column(u'main_order', 'qty_16')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'main.categorysample': {
            'Meta': {'object_name': 'CategorySample'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.imageslider': {
            'Meta': {'object_name': 'ImageSlider'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'main.order': {
            'Meta': {'object_name': 'Order'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': u"orm['auth.User']"}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': u"orm['main.Product']"}),
            'qty_1': ('django.db.models.fields.IntegerField', [], {}),
            'qty_10': ('django.db.models.fields.IntegerField', [], {}),
            'qty_12': ('django.db.models.fields.IntegerField', [], {}),
            'qty_14': ('django.db.models.fields.IntegerField', [], {}),
            'qty_16': ('django.db.models.fields.IntegerField', [], {}),
            'qty_2': ('django.db.models.fields.IntegerField', [], {}),
            'qty_3': ('django.db.models.fields.IntegerField', [], {}),
            'qty_4': ('django.db.models.fields.IntegerField', [], {}),
            'qty_6': ('django.db.models.fields.IntegerField', [], {}),
            'qty_8': ('django.db.models.fields.IntegerField', [], {})
        },
        u'main.product': {
            'Meta': {'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': u"orm['main.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        u'main.productsample': {
            'Meta': {'object_name': 'ProductSample'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products_sample'", 'to': u"orm['main.CategorySample']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'main.siteconfiguration': {
            'Meta': {'object_name': 'SiteConfiguration'},
            'active_background': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'background': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_to_notifications': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['main']