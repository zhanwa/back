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


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    openid = models.CharField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(db_column='Email', max_length=255)  # Field name made lowercase.
    image = models.CharField(max_length=255, blank=True, null=True)
    sign = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(unique=True, max_length=255)
    department = models.CharField(max_length=45, blank=True, null=True)
    label1 = models.CharField(max_length=45, blank=True, null=True)
    label2 = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class Meeting(models.Model):
    m_id = models.AutoField(primary_key=True)
    gcontent = models.CharField(db_column='gContent', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    vcontent = models.CharField(db_column='vContent', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    e_time = models.CharField(max_length=255, blank=True, null=True)
    s_time = models.CharField(max_length=255, blank=True, null=True)
    msign_id = models.CharField(max_length=255, blank=True, null=True)
    m_title = models.CharField(max_length=255, blank=True, null=True)
    c_time = models.CharField(max_length=255, blank=True, null=True)
    b_time = models.CharField(max_length=255, blank=True, null=True)
    m_place = models.CharField(max_length=255, blank=True, null=True)
    m_content = models.CharField(max_length=255, blank=True, null=True)
    mcreator_id = models.CharField(db_column='mCreator_id', max_length=255, blank=True,
                                   null=True)  # Field name made lowercase.
    mlabel = models.CharField(db_column='mLabel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    members = models.ManyToManyField(User, through='Membership')  # 多对多关联,设置在了meeting,表示meeting为理论上的主表
    status = models.NullBooleanField()  # 状态(1:开始 0:结束 空:未开始)
    limits = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.m_title

    class Meta:
        db_table = 'meeting'


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    sign = models.BooleanField(null=True, default=False)
    sign_time = models.DateTimeField(auto_now=True)  # 修改是设置为当前时间(用于保存最后创建时间) auto_now_add创建时设置当前时间(用于发布)
    admin = models.BooleanField(null=True, default=False)
    vote = models.CharField(max_length=255, blank=True, null=True)
    grade = models.CharField(max_length=255, blank=True, null=True)


class Relation(models.Model):
    r_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey('User', models.DO_NOTHING, db_column='uid', blank=True, null=True)
    m_id = models.ForeignKey('Meeting', models.DO_NOTHING, db_column='mid', blank=True, null=True)

    class Meta:
        db_table = 'relation'


# 抽奖表
class Lottery(models.Model):
    award_name = models.CharField(max_length=255, blank=True, null=True)
    award_membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    award_time = models.DateTimeField(auto_now=True)
    award_member = models.CharField(max_length=32, blank=True, null=True)
    award_leval = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.award_name


# 投票表
# 1.主题表
class Votetheme(models.Model):
    theme_name = models.CharField(max_length=255, blank=True, null=True)
    theme_id = models.CharField(max_length=32, blank=True, null=True,unique=True)
    vote_time = models.DateTimeField(auto_now_add=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return self.theme_name


# 2.选项表
class Voteoption(models.Model):
    option = models.CharField(max_length=255, blank=True, null=True)
    result = models.CharField(max_length=32, blank=True, null=True)
    votetheme = models.ForeignKey(Votetheme, to_field='theme_id', on_delete=models.CASCADE)


# 3.用户投票表
class Voteuser(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)
    answer = models.CharField(max_length=32, blank=True, null=True)
    votetheme = models.ForeignKey(Votetheme, to_field='theme_id', on_delete=models.CASCADE)
