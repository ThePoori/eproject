from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Model
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from blog.forms import TicketForm
from blog.models import *


# Create your views here.



def index(request):
    return HttpResponse("This is a index page")
#
# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.get_page(page_number)
#     except EmptyPage:
#         posts = paginator.get_page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.get_page(1)
#     context = {
#         "posts": posts
#     }
#     return render(request, "blog/list.html", context)

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = 'blog/list.html'


# def post_detail(request, id):
#     try:
#         post = Post.published.get(id = id)
#     except:
#         raise Http404("Post does not exist")
#     context = {
#         "post": post
#     }
#     return render(request, "blog/detail.html", context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'id'


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                message=cd['message'],
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject'],
            )
            return redirect("blog:index")
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {"form":form})