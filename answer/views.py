from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from requests import request
from .models import Category, FeedBack, Notification, Question, Answer, Profile, Like
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout



def Home(request):
    if request.user.is_authenticated:
        return redirect('Views_for')
    query = request.GET.get('q', None)
    list_of_question = Question.objects.all()
    if query is not None:
        list_of_question = Question.objects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(user__username__icontains=query)
        )
    return render(request, 'Homepage.html', {
        'list_of_question':list_of_question, 
    })


def questions_for_non(request):
    query = request.GET.get('q', None)
    list_of_question = Question.objects.all()
    if query is not None:
        list_of_question = Question.objects.filter(
            Q(title__icontains=query) |
            Q(category__name__icontains=query) |
            Q(user__username__icontains=query)
        )
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'index.html',
        {
            'list_of_question':list_of_question,
            'unread_notifications':unread_notifications 
        }
    )

def viewQuestion(request, slug):
    question = get_object_or_404(Question, slug=slug)

    answers = Answer.objects.filter(post_id=question).annotate(likes_count=Count("like"))

    context = {'question':question, 'answers':answers}

    return render(request, 'viewQuestion.html', context)


class EditProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = [
        'profile_image', 
        'stories', 
        'website', 
        'twitter', 
        'location',
        'city',
        ]
    template_name = 'edit.html'
    success_url = reverse_lazy('Views_for')

@login_required(login_url='login')
def profile(request, pk):
    profiles = Profile.objects.filter(user=request.user)
    questions = Question.objects.filter(user=request.user)
    number_of_likes = Like.objects.filter(post__user=request.user).count()

    context = {
        'profiles':profiles,
        'questions':questions,
        'number_of_likes':number_of_likes
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def public_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    number_of_likes = Like.objects.filter(post__user=request.user).count()
    try:
        number_of_likes = Like.objects.filter(post__user=profile.user).count()
    except ObjectDoesNotExist:
        number_of_likes = None
    context = {
        'profile':profile,
        'number_of_likes':number_of_likes
    }
    return render(request, 'public_profile.html', context)

def rules(request):
    return render(request, 'rules.html')


class My_Question(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'body', 'category']
    template_name = 'question.html'
    success_url = reverse_lazy('Views_for')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super (My_Question, self).form_valid(form)

class My_Answer(LoginRequiredMixin, CreateView):
    model = Answer
    fields = ['answer']
    template_name = 'answer.html'
    success_url = reverse_lazy('Views_for')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        result = super().form_valid(form)
        question_author = form.instance.post.user
        Notification.objects.create(user=question_author, message="someone answer your question!", url=form.instance)
        return result

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notification_list.html'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")

class FeedbackPost(CreateView):
    model = FeedBack
    fields = ['name', 'email', 'message']
    template_name = 'feedback.html'
    success_url = reverse_lazy('Thanks')

def thanks(request):

    return render(request, 'thanks.html')

def menu(request):

    return render(request, 'menu.html')

def logout_request(request):
    logout(request)
    return redirect("login")

def about(request):
    users = User.objects.all().count()
    questions = Question.objects.all().count()
    answers = Answer.objects.all().count()
    categories = Category.objects.all()
    return render(request, 'about.html', {
        'users':users,
        'questions':questions,
        'answers':answers,
        'categories':categories
    })


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('Views_for')
        else:
            messages.info(request, 'Invalid Credential') 
            return redirect('login')
    else:        
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Or Username Already Taking')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Is Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Password Not Match')
            return redirect('register')   
        return redirect ('/')     
    else:
        return render(request, 'signup.html')


def terms_of_service(request):
    
    return render (request, 'terms_of_use.html')

def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)        
    Like.objects.get_or_create(post=answer, user=request.user)    
    return redirect('view-Question', answer.post.slug)