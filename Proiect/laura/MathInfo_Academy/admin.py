from django.contrib import admin
from .models import Group, User, Abstract_Subject, Subject, Room, Interval, Week, Teacher_Subject, Teacher_Subject_Concrete, Student_Attendance
# Register your models here.

admin.site.register(Group)
admin.site.register(User)
admin.site.register(Abstract_Subject)
admin.site.register(Subject)
admin.site.register(Room)
admin.site.register(Interval)
admin.site.register(Week)
admin.site.register(Teacher_Subject)
admin.site.register(Teacher_Subject_Concrete)
admin.site.register(Student_Attendance)
