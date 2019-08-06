from django.urls import path
from . import views


app_name = 'Main'


urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login/', views.login_request, name='login'),
    path('home/', views.loggedin, name='home'),
    path('logout/', views.logout_request, name='logout')

]