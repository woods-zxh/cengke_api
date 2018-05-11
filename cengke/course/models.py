from django.db import models
from django.conf import settings

# Create your models here.

class Course(models.Model):
    data_id = models.IntegerField(default=0)
    course_id = models.IntegerField(default= 0)
    name = models.CharField(max_length= 40,blank=True)
    type = models.CharField(max_length=10,blank=True)
    school = models.CharField(max_length=30,blank=True)
    major = models.CharField(max_length=30,blank=True)
    teacher = models.CharField(max_length=20,blank=True)
    credit = models.FloatField(default=1.0)
    start_week = models.IntegerField(default=0, blank=True,)
    end_week  = models.IntegerField(default=0, blank=True,)
    gap = models.IntegerField(default=0, blank=True,)
    day_in_week = models.IntegerField(default=0, blank=True,)
    start_time = models.IntegerField(default=0, blank=True,)
    end_time = models.IntegerField(default=0, blank=True,)
    area = models.CharField(default=0, max_length=20,blank=True)
    building = models.CharField(default=0, max_length=20,blank=True)
    room = models.CharField(default=0, max_length=20,blank=True)


    class Meta:
        abstract = True


class AllCourses(Course):
    data_id = models.IntegerField(primary_key= True,default=0)
    weight = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PushMessage(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title =models.CharField(max_length= 20)
    course_time = models.CharField(max_length= 20)
    course_place = models.CharField(max_length= 20)
    introduce = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)