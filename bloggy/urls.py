from django.urls import path
from bloggy import views


app_name = 'bloggy'

urlpatterns = [
    path('', views.post_list, name='index'),
    path('post_detail/<slug:post_slug>/', views.post_detail, name='detail'),
]