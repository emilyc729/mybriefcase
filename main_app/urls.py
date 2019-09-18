from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('portfolio/create/', views.PortfolioCreate.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/update/', views.PortfolioUpdate.as_view(), name='portfolio_update'),
    path('portfolio/<int:portfolio_id>/add_photo/', views.portfolio_add_photo, name='portfolio_add_photo'),
    path('portfolio/<int:portfolio_id>/delete_photo/', views.portfolio_delete_photo, name='portfolio_delete_photo'),
    path('projects/create/', views.ProjectCreate.as_view(), name='projects_create'),
    path('projects/<int:pk>/update/', views.ProjectUpdate.as_view(), name='projects_update'),
    path('projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name='projects_delete'),
    path('projects/<int:projects_id>/add_photo/', views.projects_add_photo, name='projects_add_photo'),
    path('projects/<int:projects_id>/delete_photo/', views.projects_delete_photo, name='projects_delete_photo'),
    path('search/', views.search_portfolios, name='search_portfolios'),
    path('search/<int:user_id>/', views.search_projects, name='search_projects'),
    path('accounts/login/', views.MyLoginView.as_view(), name ='login'),
    path('accounts/signup', views.signup, name='signup')
]