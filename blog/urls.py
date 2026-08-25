from django.urls import path

from blog import views

app_name = "blog"
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('ticket/', views.ticket, name='ticket'),
]