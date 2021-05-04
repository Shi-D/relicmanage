from django.db import models

# Create your models here.
'''管理员表'''
class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)


'''文物'''
class Relic(models.Model):
    relic_name = models.CharField(max_length=128)
    dynamic = models.CharField(max_length=64, null=True)
    hot = models.IntegerField(default=0)
    picture = models.CharField(max_length=128, null=True)
    relic_file = models.CharField(max_length=256, null=True)
    other = models.CharField(max_length=256, null=True)
    type = models.CharField(max_length=256, null=True)
    is_delete = models.IntegerField(max_length=4, null=False, default='0')


'''用户'''
class Visitor(models.Model):

    user_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=11)
    sex = models.CharField(max_length=32, default='男')
    city = models.CharField(max_length=128, null=True)
    other = models.CharField(max_length=256, null=True)
    is_delete = models.IntegerField(max_length=4, null=False, default='0')


'''照片'''
class Photo(models.Model):
    # visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    photo = models.ImageField(upload_to='photo')
    relic = models.IntegerField(max_length=4, null=False, default=1)
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.IntegerField(max_length=4, null=False, default=0)


'''视频'''
class Video(models.Model):
    # visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video')
    relic_id = models.IntegerField(max_length=4, null=False, default=1)
    relic_name = models.CharField(max_length=128)
    add_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.IntegerField(max_length=4, null=False, default=0)


'''博物馆人流量记录'''
class Visits(models.Model):
    date = models.CharField(max_length=128)
    person = models.IntegerField(max_length=6, null=False, default=0)