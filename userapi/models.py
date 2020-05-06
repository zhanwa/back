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
    openid = models.CharField(unique=True, max_length=255) #openid
    username = models.CharField(unique=True, max_length=255) # 用户名
    email = models.EmailField(db_column='Email', max_length=255)  # e-mail
    image = models.ImageField(upload_to='avatarImg',null=True) # 头像
    sex = models.NullBooleanField()  # 状态(1:男 0:女 空:未填) # 性别
    sign = models.CharField(max_length=500, blank=True, null=True) #签名
    token = models.CharField(unique=True, max_length=255) #token
    address = models.CharField(max_length=255, blank=True, null=True) #地址
    label1 = models.CharField(max_length=45, blank=True, null=True) # 地区
    label2 = models.CharField(max_length=45, blank=True, null=True) # phone

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class Meeting(models.Model):
    m_id = models.AutoField(primary_key=True)
    gcontent = models.CharField(db_column='gContent', max_length=255, blank=True,
                                null=True)  # 会议类型
    vcontent = models.CharField(db_column='vContent', max_length=255, blank=True,
                                null=True)  #会议秘钥
    e_time = models.CharField(max_length=255, blank=True, null=True) #会议开始日期
    s_time = models.CharField(max_length=255, blank=True, null=True) # 会议结束日期
    msign_id = models.CharField(max_length=255, blank=True, null=True) #会议标识符
    m_title = models.CharField(max_length=255, blank=True, null=True)   #会议标题
    c_time = models.CharField(max_length=255, blank=True, null=True)    # 会议开始时间
    b_time = models.CharField(max_length=255, blank=True, null=True)   #会议结束时间
    m_place = models.CharField(max_length=255, blank=True, null=True) # 会议地点
    m_content = models.CharField(max_length=255, blank=True, null=True) #会议简介
    mcreator_id = models.CharField(db_column='mCreator_id', max_length=255, blank=True,
                                   null=True)  # 创建者id
    mlabel = models.CharField(db_column='mLabel', max_length=255, blank=True, null=True)  # 会议标签
    members = models.ManyToManyField(User, through='Membership')  # 多对多关联,设置在了meeting,表示meeting为理论上的主表
    status = models.NullBooleanField()  # 状态(1:开始 0:结束 空:未开始)
    limits = models.CharField(max_length=255, default='')# 会议限制人数

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



# 抽奖表
class Lottery(models.Model):
    award_name = models.CharField(max_length=255, blank=True, null=True) #奖品名称及数量[{award:'',num:''}]
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE) # 外键关联会议
    award_time = models.DateTimeField(auto_now=True) # 发起时间
    award_member = models.CharField(max_length=32, blank=True, null=True) #抽取人数
    award_leval = models.CharField(max_length=32, blank=True, null=True) #抽奖等级
    award_type =  models.CharField(max_length=32, blank=True, null=True) #抽奖方式
    award_membership = models.ManyToManyField(User)

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


# 文件表
class Document(models.Model):
    Dname = models.CharField(max_length=255, blank=True, null=True) # 文件名字
    Dtime = models.DateTimeField(auto_now_add=True) # 上传时间
    Dstyle = models.CharField(max_length=32, blank=True, null=True) # 文件类型 ppt img word等
    Dsize = models.CharField(max_length=32, blank=True, null=True) #文件大小
    Dpath = models.CharField(max_length=255, blank=True, null=True) # 文件路径
    Dstatus = models.BooleanField(null=True, default=True) # 是够可下载,默认可以
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    objects = models.Manager()
    def __str__(self):
        return self.Dname
# 收藏表
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 多对一 一个用户可收藏多个东西
    product_name = models.CharField(max_length=255, blank=True, null=True) # 名称,冗余设计
    product_type = models.CharField(max_length=255, blank=True, null=True) #类型
    product_id = models.CharField(max_length=32, blank=True, null=True) #产品id
    collect_time = models.DateTimeField(auto_now=True) # 收藏时间

# 签到表
class Usersign(models.Model):
    Stime = models.DateTimeField(auto_now_add=True) # 签到时间
    Snumber = models.CharField(max_length=32) #签到号码(学号或工号)
    Sdepartment = models.CharField(max_length=255) #签到部门或班级
    membership = models.OneToOneField(to='Membership', on_delete=models.CASCADE) # Membership从表,用来记录签到信息
