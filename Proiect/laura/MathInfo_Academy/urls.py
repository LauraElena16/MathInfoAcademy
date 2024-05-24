from django.urls import path
from . import views
 
urlpatterns = [ 
    path('', views.home, name='home'),
    # path('test/', views.test, name='test'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('directions/', views.directions, name='directions')
    # path pentru pagina cu directii
]