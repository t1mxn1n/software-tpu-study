from django.urls import path
from study_app import views


urlpatterns = [
    path('', views.index),
    path('ads/<int:ad_id>', views.ads, name='ads'),
    path('ads/', views.ads_general, name='ads_general')
]
