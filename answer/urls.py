from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('login', views.login, name='login'),
    path('questions/<slug:slug>/', views.viewQuestion, name='view-Question'),
    path('question/<int:pk>/answer/', views.My_Answer.as_view(), name='answer'),
    path('question/', views.My_Question.as_view(), name='question'),
    path('register/', views.register, name='register'),
    path('feedback/', views.FeedbackPost.as_view(), name='FeedBack'),
    path('notification/', views.NotificationListView.as_view(), name='notification'),
    path('profile/<int:pk>/', views.profile, name='Profile'),
    path('edit/<slug:slug>/', views.EditProfile.as_view(), name='edit'),
    path('userProfile/<slug:slug>/', views.public_profile, name='Public_Profile'),
    path('Privacy-policy', views.rules, name='Rules'),
    path('answer/<int:pk>/like', views.like_answer, name='like-answer'),
    path('about/', views.about, name='About'),
    path('Terms-Of-Use/', views.terms_of_service, name='Terms'),
    path('index', views.questions_for_non, name='Views_for'),
    path('thanks-page', views.thanks, name='Thanks'),
    path('menu/', views.menu, name='Menu'),
    path("logout", views.logout_request, name="logout"),
]