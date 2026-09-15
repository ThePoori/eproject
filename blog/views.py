from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Model
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from blog.forms import *
from blog.models import *
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.contrib.auth import authenticate, login, logout

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

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file = form.cleaned_data['image1'], post = post)
            Image.objects.create(image_file = form.cleaned_data['image2'], post = post)
            return redirect("blog:profile")
    else:
        form = CreatePostForm()
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

@login_required
def profile(request):
    user = request.user
    post = Post.published.filter(author=user)
    context = {
        "post": post
    }
    return render(request, "blog/profile.html", context)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect("blog:profile")
    return render(request, "forms/delete_post.html", {"post": post})

@login_required
def delete_image(request, image_id):
    img = get_object_or_404(Image, id=image_id)
    img.delete()
    return redirect("blog:profile")

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect("blog:profile")
    else:
        form = CreatePostForm(instance = post)
    return render(request, "forms/create_post.html", {"form": form, "post": post})


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect("blog:profile")
#                 else:
#                     return HttpResponse("Your account has been disabled")
#             else:
#                 return HttpResponse("Invalid login details supplied")
#     else:
#         form = LoginForm()
#     return render(request, "registration/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, "registration/register_done.html", {'user': user})
    else:
        form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})