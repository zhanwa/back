
from django.db import models


class CoCachedMessage(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    cached_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'co_cached_message'


class Friends(models.Model):
    fid = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=800, blank=True, null=True)
    sign = models.CharField(max_length=500, blank=True, null=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)

    class Meta:
        db_table = 'friends'


class Meeting(models.Model):
    m_id = models.AutoField(primary_key=True)
    gcontent = models.CharField(db_column='gContent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vcontent = models.CharField(db_column='vContent', max_length=255, blank=True, null=True)  # Field name made lowercase.
    e_time = models.CharField(max_length=255, blank=True, null=True)
    s_time = models.CharField(max_length=255, blank=True, null=True)
    msign_id = models.CharField(max_length=255, blank=True, null=True)
    m_title = models.CharField(max_length=255, blank=True, null=True)
    c_time = models.CharField(max_length=255, blank=True, null=True)
    b_time = models.CharField(max_length=255, blank=True, null=True)
    m_place = models.CharField(max_length=255, blank=True, null=True)
    m_content = models.CharField(max_length=255, blank=True, null=True)
    mcreator_id = models.CharField(db_column='mCreator_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mlabel = models.CharField(db_column='mLabel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    objects = models.Manager()
    class Meta:
        db_table = 'meeting'


class MeetingUser(models.Model):
    m_id = models.ForeignKey('Meeting', models.DO_NOTHING)
    cu_id = models.IntegerField()
    sign = models.PositiveIntegerField(blank=True, null=True)
    admin = models.PositiveIntegerField(blank=True, null=True)
    vote = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'meeting_user'
        unique_together = (('m_id', 'cu_id'),)


class Relation(models.Model):
    r_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    m_id = models.ForeignKey('Meeting', models.DO_NOTHING, db_column='mid', blank=True, null=True)

    class Meta:
        db_table = 'relation'


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    openid = models.CharField(unique=True,max_length=255)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(db_column='Email', max_length=255)  # Field name made lowercase.
    image = models.CharField(max_length=255, blank=True, null=True)
    sign = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(unique=True, max_length=255)
    department = models.CharField(max_length=45, blank=True, null=True)
    label1 = models.CharField(max_length=45, blank=True, null=True)
    label2 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'user'
