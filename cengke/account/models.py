from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


#
# class Course(models.Model):
#     course_id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length= 40)
#     type = models.CharField(max_length=10)
#     school = models.CharField(max_length=30)
#     major = models.CharField(max_length=30,blank=True)
#     teacher = models.CharField(max_length=20)

class Nuser(AbstractUser):
    sigh = models.CharField(max_length=100,default="I am goo!")
    # school = models.CharField(max_length=20,default="0")
    # year = models.IntegerField(default=2018)
    # table_time = models.DateTimeField(default=timezone.now)
    # couese_table = models.ForeignKey(Course,on_delete=models.CASCADE())
    # course_recom = models.ForeignKey(Course,on_delete=models.CASCADE())
    # course_colle = models.ForeignKey(Course,on_delete=models.CASCADE())

