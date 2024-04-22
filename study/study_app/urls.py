from django.urls import path
from study_app import views


urlpatterns = [
    path('', views.index),
    path('ads/<int:ad_id>', views.ads, name='ads'),
    path('ads/', views.ads_general, name='ads_general'),
    path('test/', views.test, name='test'),
    path('personal/', views.personal, name='personal'),
    path('register/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login')
]
