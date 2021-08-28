from django.urls import path

from . import views_api

urlpatterns = [
    path('login/', views_api.LoginView.as_view()),
    path('register/', views_api.RegisterView.as_view()),
    path('addcomment/', views_api.AddCommentView.as_view()),
    path('addlike/', views_api.AddLikeView.as_view()),
]
