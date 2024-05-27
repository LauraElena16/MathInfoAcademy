from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.



class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    def __str__(self):
        return self.id
    

class Activity_Type(models.TextChoices):
    LECTURE = 'lecture', 'Lecture'
    SEMINAR = 'seminar', 'Seminar'
    LABORATORY = 'laboratory', 'Laboratory'



class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    credits = models.IntegerField()
    def __str__(self):
        return self.name


class Teacher_Activity(models.Model):
    id = models.AutoField(primary_key=True)
    activity_type = models.CharField(max_length=10, choices=Activity_Type.choices, default=Activity_Type.LECTURE)
    max_grade = models.FloatField()
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.id


def documentation_upload_path(instance, filename):
    id = instance.teacher_activity.id
    return f'documentations/{id}/{filename}'


class Materials(models.Model):
    id = models.AutoField(primary_key=True)
    documentation = models.FileField(upload_to=documentation_upload_path, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    teacher_activity = models.ForeignKey(Teacher_Activity, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.id


class Students_Activity(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    teacher_activity = models.ForeignKey(Teacher_Activity, on_delete=models.SET_NULL, null=True)
    grade = models.FloatField()
    def __str__(self):
        return self.id




