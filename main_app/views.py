from django.shortcuts import render, redirect
from .models import User, Portfolio, Project
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.views import LoginView
# photos
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'dogcollector-ec'

def home(request):
    users = User.objects.all()
    projects = {}
    portfolios = {}
    for u in users:
        if Portfolio.objects.filter(user_id=u.id).exists():
            projects = Project.objects.all().order_by('date')
            portfolios = Portfolio.objects.all()
    return render(request, 'home.html', {'users': users, 'projects':projects, 'portfolios':portfolios})
          

def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    if Portfolio.objects.filter(user_id=user.id).exists():
        portfolio_id = user.portfolio
        projects = Project.objects.filter(portfolio=portfolio_id).order_by('date')
        return render(request, 'main_app/user_profile.html', {'user': user, 'projects':projects})
    else:
        return render(request, 'main_app/user_profile.html', {'user': user})

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

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_profile', kwargs={'user_id': user_id})


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

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = [
        'project_name',
        'technologies',
        'deployed_link',
        'project_link',
        'description',
    ]

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_profile', kwargs={'user_id': user_id})
 
    def form_valid(self, form):
        form.instance.date = self.request.POST['date']
        form.instance.portfolio = self.request.user.portfolio
        return super().form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = [
        'project_name',
        'technologies',
        'deployed_link',
        'project_link',
        'description',
    ]

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_profile', kwargs={'user_id': user_id})

    def form_valid(self, form):
        form.instance.date = self.request.POST['date']
        return super().form_valid(form)

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = "main_app/projects_confirm_delete.html"

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

def search_portfolios(request):
    search_content = request.GET.get('search_content')
    option = request.GET.get('option')
    if option == 'profession' and search_content:
        portfolios = Portfolio.objects.filter(profession__icontains=search_content)
        users = []
        projects = []
        for p in portfolios:
            for proj in p.project_set.all():
                projects.append(proj)
            users.append(p.user)
        return render(request, 'home.html', {'users':users, 'projects':projects, 'portfolios':portfolios})
    if option == 'technologies' and search_content:
        projects = Project.objects.filter(technologies__icontains=search_content)
        plist = []
        ulist = []
        for p in projects:
            plist.append(p.portfolio)
            ulist.append(p.portfolio.user)
      
        portfolios = set(plist)
        users = set(ulist)
        return render(request, 'home.html', {'users':users, 'projects':projects, 'portfolios':portfolios})

def search_projects(request, user_id):
    search_content = request.GET.get('search_content')
    user = User.objects.get(id=user_id)
    projects = Project.objects.filter(technologies__icontains=search_content, portfolio=user.portfolio)
    return render(request, 'main_app/user_profile.html', {'user': user, 'projects':projects})


class MyLoginView(LoginView):
    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user_profile', kwargs={'user_id': user_id})

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
            return redirect('user_profile', user.id)
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


