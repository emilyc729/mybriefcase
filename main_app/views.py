from django.shortcuts import render, redirect
from .models import User, Portfolio, Photo, Project
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
    return render(request, 'main_app/user_profile.html', {'user': user})

class PortfolioPage(LoginRequiredMixin, ListView):
    model = Portfolio
    context_object_name = 'portfolios'

class PortfolioCreate(LoginRequiredMixin, CreateView):
    model = Portfolio
    fields = ['profession', 'profile_link', 'github_link', 'about_me']
    success_url = '/portfolio/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PortfolioDetail(LoginRequiredMixin, DetailView):
    model = Portfolio
    
@login_required
def add_photo(request, portfolio_id):
    photo_file = request.FILES.get('photo-file', None)
    portfolio = Portfolio.objects.get(id=portfolio_id)
    print(portfolio)
    # make sure a file is uploaded
    if photo_file:
        s3 = boto3.client('s3')
 
        # random # + file extension(.jpg, .png)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            portfolio.photo_url = url
            print(f'photo url : {portfolio.photo_url}')
            portfolio.update(update_fields=['photo_url'])
        except:
            print('An error occurred uploading file to s3')
    return redirect(portfolio)


#sign up view
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

def assoc_project(request, portfolio_id, project_id):
    Portfolio.objects.get(id=portfolio_id).projects.add(project_id)
    return redirect('detail', portfolio_id=portfolio_id)

def unassoc_project(request, portfolio_id, project_id):
    Portfolio.objects.get(id=portfolio_id).projects.remove(project_id)
    return redirect('detail', portfolio_id=portfolio_id)

class ProjectList(ListView):
    model = Project 

class ProjectDetail(DetailView):
    model = Project 

class ProjectCreate(CreateView):
    model = Project 
    fields = [
        'portfolio', 
        'project_name', 
        'technologies', 
        'deployed_link', 
        'project_link', 
        'description', 
        'date'
    ]

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
    success_url = '/projects/'



