from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Model
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from blog.forms import TicketForm, CommentForm, PostForm, SearchForm
from blog.models import *
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


# Create your views here.



def index(request):
    return render(request, "blog/index.html")
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


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }
    return render(request, "blog/detail.html", context)


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#     pk_url_kwarg = 'id'


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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        "post": post,
        "comment": comment,
        "form": form,
    }
    return render(request, "forms/comment.html", context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("blog:index")
    else:
        form = PostForm()
    return render(request, "forms/create_post.html", {"form": form})


def post_search(request):
    query = None
    post_results = []
    image_results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            post_result1 = Post.published.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0)
            post_result2 = Post.published.annotate(similarity=TrigramSimilarity('description', query)).filter(similarity__gt=0)
            post_results = (post_result1 | post_result2).order_by('-similarity')
            image_result1 = Image.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0)
            image_result2 = Image.objects.annotate(similarity=TrigramSimilarity('description', query)).filter(similarity__gt=0)
            image_results = (image_result1 | image_result2).order_by('-similarity')
    context = {
        "query": query,
        "post_results": post_results,
        "image_results": image_results,
    }
    return render(request, 'blog/search.html', context)


