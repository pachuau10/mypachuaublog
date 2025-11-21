from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    # urls.py
    path('about/', views.about, name='about'),
    path("contact/", views.contact, name="contact"),
   

]
