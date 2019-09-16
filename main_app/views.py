from django.shortcuts import render, redirect
from .models import User, Portfolio, Project
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
# photos
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'dogcollector-ec'


def home(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users})


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    portfolio_id = user.id
    projects = Project.objects.filter(portfolio_id=portfolio_id)
    print(projects)
    return render(request, 'main_app/user_profile.html', {'user': user, 'projects':projects})

class PortfolioCreate(LoginRequiredMixin, CreateView):
    model = Portfolio
    fields = ['profession', 'profile_link', 'github_link', 'about_me']

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_profile', kwargs={'user_id': user_id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PortfolioUpdate(LoginRequiredMixin, UpdateView):
    model = Portfolio
    fields = ['profession', 'profile_link', 'github_link', 'about_me']


@login_required
def portfolio_add_photo(request, portfolio_id):
    photo_file = request.FILES.get('photo-file', None)
    portfolio = Portfolio.objects.get(id=portfolio_id)
    user = User.objects.get(id=request.user.id).id
    # make sure a file is uploaded
    if photo_file:
        s3 = boto3.client('s3')
        # random # + file extension(.jpg, .png)
        key = uuid.uuid4().hex[:6] + \
                         photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            portfolio.photo_url = url
            portfolio.save()
        except:
            print('An error occurred uploading file to s3')
    return redirect('user_profile', user)


@login_required
def portfolio_delete_photo(request, portfolio_id):
    user = User.objects.get(id=request.user.id).id
    portfolio = Portfolio.objects.get(id=portfolio_id)
    portfolio.photo_url = ''
    portfolio.save()
    return redirect('user_profile', user)


# sign up view
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class ProjectCreate(CreateView):
    model = Project
    fields = [
        'project_name',
        'technologies',
        'deployed_link',
        'project_link',
        'description',
        'date'
    ]

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_profile', kwargs={'user_id': user_id})

    def form_valid(self, form):
        form.instance.portfolio = self.request.user.portfolio
        return super().form_valid(form)


class ProjectUpdate(UpdateView):
    model = Project
    fields = [
        'project_name',
        'technologies',
        'deployed_link',
        'project_link',
        'description',
        'date'
    ]


class ProjectDelete(DeleteView):
    model = Project

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_profile', kwargs={'user_id': user_id})

@login_required
def projects_add_photo(request, projects_id):
    photo_file = request.FILES.get('photo-file', None)
    projects = Project.objects.get(id=projects_id)
    user = User.objects.get(id=request.user.id).id
    # make sure a file is uploaded
    if photo_file:
        s3 = boto3.client('s3')
        # random # + file extension(.jpg, .png)
        key = uuid.uuid4().hex[:6] + \
                         photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            projects.photo_url = url
            projects.save()
        except:
            print('An error occurred uploading file to s3')
    return redirect('user_profile', user)


@login_required
def projects_delete_photo(request, projects_id):
    user = User.objects.get(id=request.user.id).id
    projects = Project.objects.get(id=projects_id)
    projects.photo_url = ''
    projects.save()
    return redirect('user_profile', user)
