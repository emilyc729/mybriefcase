from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('portfolio/', views.PortfolioPage.as_view(), name='portfolio'),
    path('portfolio/<int:pk>/', views.PortfolioDetail.as_view(), name='portfolio_detail'),
    path('portfolio/create/', views.PortfolioCreate.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/update/', views.PortfolioUpdate.as_view(), name='portfolio_update'),
    path('portfolio/<int:portfolio_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup', views.signup, name='signup')
]