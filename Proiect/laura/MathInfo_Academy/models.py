from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    email = models.EmailField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    

class Activity_Type(models.TextChoices):
    LECTURE = 'lecture', 'Lecture'
    SEMINAR = 'seminar', 'Seminar'
    LABORATORY = 'laboratory', 'Laboratory'



class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    credits = models.IntegerField()
    def __str__(self):
        return self.name


class Teacher_Activity(models.Model):
    id = models.AutoField(primary_key=True)
    activity_type = models.CharField(max_length=10, choices=Activity_Type.choices, default=Activity_Type.LECTURE)
    max_grade = models.FloatField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.teacher.username}, {self.course.name}, {self.activity_type}"


def documentation_upload_path(instance, filename):
    id = instance.teacher_activity.id
    return f'documentations/{id}/{filename}'


class Materials(models.Model):
    id = models.AutoField(primary_key=True)
    documentation = models.FileField(upload_to=documentation_upload_path, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    teacher_activity = models.ForeignKey(Teacher_Activity, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.teacher_activity.activity_type}, {self.teacher_activity.course.name}, {self.teacher_activity.teacher.username}"


class Students_Activity(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    teacher_activity = models.ForeignKey(Teacher_Activity, on_delete=models.CASCADE, null=True)
    grade = models.FloatField()
    def __str__(self):
        return f"{self.student.username}, {self.teacher_activity.course.name}, {self.teacher_activity.activity_type}"




