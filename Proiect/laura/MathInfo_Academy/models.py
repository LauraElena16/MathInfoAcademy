from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.id
    

class Subject_Type(models.TextChoices):
    LECTURE = 'lecture', 'Lecture'
    SEMINAR = 'seminar', 'Seminar'
    LABORATORY = 'laboratory', 'Laboratory'


class Abstract_Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(
        max_length=10,
        choices=Subject_Type.choices,
        default=Subject_Type.LECTURE,
    )
    abstract_subject = models.ForeignKey(Abstract_Subject, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.id
    

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    no_seats = models.IntegerField()
    def __str__(self):
        return self.name
    

class Interval(models.Model):
    id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    day = models.CharField(max_length=50)
    def __str__(self):
        return self.id


class Week(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_even = models.BooleanField(default=False)
    def __str__(self):
        return self.id


class Teacher_Subject(models.Model):
    id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    interval = models.ForeignKey(Interval, on_delete=models.SET_NULL, null=True)
    groups = models.ManyToManyField(Group)
    students_optionals = models.ManyToManyField(User, related_name='students_optionals')
    week = models.ManyToManyField(Week, through='Teacher_Subject_Concrete')
    def __str__(self):
        return self.id


def documentation_upload_path(instance, filename):
    teacher_id = instance.teacher_subject.teacher.id
    subject_id = instance.teacher_subject.subject.id
    week_id = instance.week.id
    return f'documentations/{teacher_id}/{subject_id}/{week_id}/{filename}'


class Teacher_Subject_Concrete(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_subject = models.ForeignKey(Teacher_Subject, on_delete=models.SET_NULL, null=True)
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    documentation = models.FileField(upload_to=documentation_upload_path, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    students_present_concrete = models.ManyToManyField(User, through='Student_Attendance')
    def __str__(self):
        return self.id
    

class Student_Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    teachers_subjects_concrete = models.ForeignKey(Teacher_Subject_Concrete, on_delete=models.CASCADE)
    points = models.FloatField()

    
# class Students_Present_Concrete(models.Model):
#     teachers_subjects_concrete = models.ForeignKey(Teacher_Subject_Concrete)
#     student = models.ForeignKey(User)



# class Students_Optionals(models.Model):
#     student = models.ForeignKey(User)
#     teacher_subject = models.ForeignKey(Teacher_Subject)
#     def __str__(self):
#         return self.id
    

# class Groups_Courses(models.Model):
#     group = models.ForeignKey(Group)
#     teacher_subject = models.ForeignKey(Teacher_Subject)
#     def __str__(self):
#         return self.id