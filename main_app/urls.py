from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('portfolio/', views.PortfolioPage.as_view(), name='portfolio'),
    path('portfolio/create/', views.PortfolioCreate.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/', views.PortfolioDetail.as_view(), name='portfolio_detail'),
    path('portfolio/<int:portfolio_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup', views.signup, name='signup')
    # associate a project with a portfolio 
    path('portfolio/<int:portfolio_id>/assoc_project/<int:project_id>/', views.assoc_project, name='assoc_project'),
    # unassociate a project and portfolio
    path('portfolio/<int:portfolio_id>/unassoc_project/<int:project_id>/', views.unassoc_project, name='unassoc_project'),
    path('projects/', views.ProjectList.as_view(), name='projects_index'),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='projects_detail'),
    
]