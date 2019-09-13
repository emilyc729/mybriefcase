from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


#Portfolio Model
class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_link = models.CharField(max_length=100) #like a LinkedIn or SocialMedia Link
    github_link = models.CharField(max_length=100) #main github page that shows all repositories
    about_me = models.TextField(max_length=800) #description about user: interests/hobbies/goals
    

    def __str__(self):
        return f'{self.id} portfolio'
    
    def get_absolute_url(self): 
        return reverse('portfolio', kwargs={'pk':self.id})

#Project Model
class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=20)   
    technologies = models.TextField(max_length=200) #list of technologies used
    deployed_link = models.CharField(max_length=100) #where project is deployed 
    project_link = models.CharField(max_length=100) #project's github link
    description = models.TextField(max_length=300)  #dmodelsate completed project
    date = models.DateField()

    def __str__(self):
        return f'{self.portfolio.user} Project: {self.id} {self.project}'

#Photo Model
class Photo(models.Model):
    portfolio_photo = models.OneToOneField(Portfolio, on_delete = models.CASCADE)
    project_photo = models.OneToOneField(Project, on_delete = models.CASCADE)
    url = models.CharField(max_length=200)  #photo url

    def __str__(self):
        return f'{self.url}'