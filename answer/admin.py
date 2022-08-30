from django.contrib import admin
from .models import Answer, FeedBack, Question, Notification, Category, Profile, Like

# Register your models here.

admin.site.register(Answer)
admin.site.register(FeedBack)
admin.site.register(Question)
admin.site.register(Notification)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Like)
