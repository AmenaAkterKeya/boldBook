from django.urls import path
from . import views
urlpatterns = [
    path('',views.home , name='home'),
    path('categories/<slug:catagory_slug>/', views.home, name='catagory_wise_post'),
]