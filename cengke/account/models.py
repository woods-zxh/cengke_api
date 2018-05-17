from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from course.models import Course




class Nuser(AbstractUser):
    real_name = models.CharField(max_length=10,default="woods")
    sigh = models.CharField(max_length=100, default="I am good!")
    school = models.CharField(max_length=20, default="0")
    grade = models.IntegerField(default=2018)
    table_time = models.DateTimeField(auto_now_add=True)
    can_post = models.BooleanField(default=False)
    term = models.CharField(max_length=20, default="0")
    week = models.CharField(max_length=20, default="0")

    def __str__(self):
        return self.username

class CourseTable(models.Model):
    # id = models.IntegerField(default=0,primary_key=True)
    user = models.ForeignKey(Nuser, on_delete=models.CASCADE)
    course_id = models.IntegerField()

    def __str__(self):
        return self.user.username

class Coursecolle(models.Model):
    # id = models.IntegerField(default=0,primary_key=True)
    course_id = models.IntegerField()
    user = models.ForeignKey(Nuser, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Coursehistory(models.Model):
    # id = models.IntegerField(default=0,primary_key=True)
    user = models.ForeignKey(Nuser, on_delete=models.CASCADE)
    course_id = models.IntegerField()
    comment = models.CharField(max_length=200,default="写点什么吧！")

    def __str__(self):
        return self.user.username


# a.coursetable_set.create(name = "高等数学B1" ,type = "专业必修",school = "计算机学院" , major = "software",teacher="woods",credit = "1.0",start_week=2,end_week = 12,gap = 0,day_in_week = 4,start_time = 9,end_time = 11,area = 3, building = 301,room = 101)
