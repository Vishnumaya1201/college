from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class staff(models.Model):
    st_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    st_address = models.CharField(max_length=255)
    st_gender = models.CharField(max_length=255)
    st_phone = models.CharField(max_length=255)
    st_photo = models.ImageField(upload_to="image/", null=True)

    def __str__(self):
        return self.st_phone


class course(models.Model):
    course_name = models.CharField(max_length=225)
    course_fee = models.IntegerField()

    def __str__(self):
        return self.course_name


class student(models.Model):
    std_course = models.ForeignKey(course, on_delete=models.CASCADE, null=True)
    std_name = models.CharField(max_length=225)
    std_address = models.CharField(max_length=225)
    std_age = models.IntegerField()
    std_joindate = models.DateField()

    def __str__(self):
        return self.std_name