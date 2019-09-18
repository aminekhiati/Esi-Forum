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
    path('users', views.UsersListView.as_view(), name='users'),
    path('approveuser/<int:pk>', views.approverUser, name='approve'),
    path('supprimeruser/<int:pk>', views.supprimerUser, name='supprime'),
    path('updateuser/<int:pk>', views.updateUser, name='updateuseradmin'),
    path('addmod/', views.addmod, name='addmod'),
    path('username', views.searchUser, name='searchuserdashboard'),
    path('unban/<int:pk>', views.unban, name='unban'),
    path('ban/<int:pk>', views.ban, name='ban'),
    path('selectrole', views.selectrole, name='selectrole'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('usersettings/', views.editeProfile, name='editprofile'),
    path('searchresults/',views.search, name='search'),
    path('userpage/<int:pk>',views.userpage, name='userpage'),
    path('engpub/<int:pk>',views.enrigstre_pub,name='engpub'),
    path('reports/',views.ReportListView.as_view(),name='reports'),
    path('reports/delete/<int:pk>',views.ReportDeleteView.as_view(),name='report-delete'),
    path('reports/deletemeesage/<int:pk>',views.MessageDeleteView.as_view(),name='message-delete'),
    path('', views.redirect_offtalk, name='home'),
    path('message/new/', views.add_message, name='message-new'),
    path('<str:category>/section/', views.redirect_type, name='redirect-type'),
    path('<str:category>/', PostListView.as_view(), name='category'),
    path('<str:category>/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<str:category>/post/new/', PostCreateView.as_view(), name='post-create'),
    path('<str:category>/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<str:category>/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<str:category>/post/<int:pk>/comment/new/', views.add_comment_to_post, name='comment-new'),
    path('<str:category>/post/<int:pk1>/comment/delete/<int:pk2>/', views.comment_remove, name='comment-delete'),
    path('<str:category>/post/<int:pk1>/comment/update/<int:pk2>/', views.comment_update, name='comment-update'),
    path('<str:category>/clear-notifications/', views.clear_notifications, name='clear-notifications')
]