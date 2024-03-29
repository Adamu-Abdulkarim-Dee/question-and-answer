from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    
    def __str__(self):
        return str(self.name)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    body = RichTextField(blank=False, null=False) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=200)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)

class Answer(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    answer = RichTextField(blank=False, null=False)
    post = models.ForeignKey(Question, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)  

class FeedBack(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(blank=False, null=False)

    def __str__(self):
       return str(self.name)


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
       return str(self.user)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', blank=True, null=True, default='static/default.jpg')
    stories = RichTextField(blank=True, null=True)
    twitter = models.URLField(max_length=300, blank=True, null=True)
    website = models.URLField(max_length=300,blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=80, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=200)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)