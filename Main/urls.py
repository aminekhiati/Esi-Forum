from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentUpdateView,
    
)




urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('edituser', views.dashboard_editProfile, name='edituser'),
    path('users', views.users, name='users'),
    path('login/', views.login_request, name='login'),
    path('home/', views.loggedin, name=''),
    path('logout/', views.logout_request, name='logout'),
    path('usersettings/', views.editeProfile, name='editprofile'),
    path('searchresults',views.search, name='search'),

    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/new/', views.add_comment_to_post, name='comment-new'),
    path('post/<int:pk1>/comment/delete/<int:pk2>/', views.comment_remove, name='comment-delete'),
    path('post/<int:pk1>/comment/update/<int:pk2>/', views.comment_update, name='comment-update'),
    
]