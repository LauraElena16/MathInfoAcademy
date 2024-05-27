from django.contrib import admin
from .models import Materials, Students_Activity, Subject, Teacher_Activity, User
# Register your models here.

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Teacher_Activity)
admin.site.register(Materials)
admin.site.register(Students_Activity)
