from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

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

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),      
]