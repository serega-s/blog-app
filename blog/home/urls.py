from django.urls import path

from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.Home.as_view(), name='home'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    # path('add-post/', views.add_post, name='add_post'),
    path('add-post/', views.AddPost.as_view(), name='add_post'),
    path('post-detail/<slug:slug>/', views.post_detail, name="post_detail"),
    # path('post-delete/<int:id>/', views.post_delete, name="post_delete"),
    path('post-delete/<int:id>/', views.PostDelete.as_view(), name="post_delete"),
    # path('post-update/<slug:slug>/', views.post_update, name="post_update"),
    path('post-update/<slug:slug>/', views.PostUpdate.as_view(), name="post_update"),
    # path('user-posts/', views.user_posts, name='user_posts'),
    path('user-posts/', views.UserPosts.as_view(), name='user_posts'),
    path('verify/<str:token>/', views.verify, name='verify'),
]
