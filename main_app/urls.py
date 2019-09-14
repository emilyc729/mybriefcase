from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('portfolio/', views.PortfolioPage.as_view(), name='portfolio'),
    path('portfolio/create/', views.PortfolioCreate.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/', views.PortfolioDetail.as_view(), name='portfolio_detail'),
    path('portfolio/<int:portfolio_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup', views.signup, name='signup')
]