# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Catlist(models.Model):
    category = models.CharField(primary_key = True, db_column='CATEGORY', max_length=100, blank=True, null = False)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    resources = models.CharField(db_column='RESOURCES', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    calendar = models.CharField(db_column='CALENDAR', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'catList'


class Mainbae(models.Model):
    name = models.CharField(primary_key = True, db_column='NAME', max_length=100, blank=True, null = False)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    start = models.DateTimeField(db_column='START', blank=True, null=True)  # Field name made lowercase.
    end = models.DateTimeField(db_column='END', blank=True, null=True)  # Field name made lowercase.
    info = models.CharField(db_column='INFO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    cancelled = models.IntegerField(db_column='CANCELLED', blank=True, null=True)  # Field name made lowercase.
    updated = models.IntegerField(db_column='UPDATED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'mainBae'
