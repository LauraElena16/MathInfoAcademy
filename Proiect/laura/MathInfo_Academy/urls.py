from django.urls import path
from . import views
 
urlpatterns = [ 
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('directions/', views.directions, name='directions'),
    path('activity/', views.activity, name='register'),
    path('grades/', views.grades, name='grades'),
    path('register/', views.register, name='register'),
    path('upload_material/<str:course_name>/<str:activity_type>/', views.upload_material, name='upload_material'),
    path('delete_material/<int:material_id>/', views.delete_material, name='delete_material'),
    path('grade_student/<int:student_activity_id>/', views.grade_student, name='grade_student'),
    path('modify_max_grade/<int:teacher_activity_id>/', views.modify_max_grade, name='modify_max_grade'),
]