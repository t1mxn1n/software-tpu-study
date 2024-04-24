from django.contrib.auth.views import LogoutView
from django.urls import path, include
from study_app import views


urlpatterns = [
    path('', views.index),
    # path('ads/<int:ad_id>', views.ads, name='ads'),
    path('ads/', views.ads_general, name='ads_general'),
    path('lk/', views.personal, name='personal'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
