from django.urls import path
from bloggy import views


app_name = 'bloggy'

urlpatterns = [
    # path('', views.post_list, name='index'),
    # modify for class-based views
    path('', views.PostListView.as_view(), name='index'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_detail, name='detail'),
    path('<int:post_id>/share/', views.post_share, name='share'),
]
