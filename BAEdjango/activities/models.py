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
from django.contrib.auth.models import User


class Writers(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Writers'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

class BAEUser(models.Model):
    user = models.OneToOneField(User)
    skating = models.BooleanField()
    watching = models.BooleanField()
    basketball = models.BooleanField()
    martial = models.BooleanField()
    stephens = models.BooleanField()
    dillon = models.BooleanField()
    swimming = models.BooleanField()
    squash = models.BooleanField()
    tennis = models.BooleanField()
    running = models.BooleanField()
    fitness = models.BooleanField()
    oa = models.BooleanField()
    dance = models.BooleanField()
    biking = models.BooleanField()
    yoga = models.BooleanField()


class Catlist(models.Model):
    category = models.CharField(db_column='CATEGORY', max_length=100, blank=True, primary_key = True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    resources = models.CharField(db_column='RESOURCES', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    calendar = models.CharField(db_column='CALENDAR', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'catList'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Mainbae(models.Model):
    name = models.CharField(db_column='NAME', max_length=100, blank=True, primary_key = True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=100, blank=True, null=True)  # Field name made lowercase.
    start = models.DateTimeField(db_column='START', blank=True, null=True)  # Field name made lowercase.
    end = models.DateTimeField(db_column='END', blank=True, null=True)  # Field name made lowercase.
    info = models.CharField(db_column='INFO', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    cancelled = models.IntegerField(db_column='CANCELLED', blank=True, null=True)  # Field name made lowercase.
    updated = models.IntegerField(db_column='UPDATED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mainBae'
