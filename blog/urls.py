from django.urls import path

from blog import views

app_name = "blog"
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<post_id>/comment/', views.post_comment, name='post_comment'),
    path('ticket/', views.ticket, name='ticket'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.post_search, name='post_search'),
    path('profile/', views.profile, name='profile'),
]