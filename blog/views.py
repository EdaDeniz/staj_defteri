from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.contrib.auth.views import login
from django.db.models import Q
from django.forms import model_to_dict
from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from requests import post
from .forms import PostForm, CommentForm
from django.shortcuts import get_object_or_404
from blog.models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from blog.forms import SignUpForm
from django.views import View


class PostComment(View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.all()
        form = CommentForm()
        context = {
            'post': post,
            'comments': comments,
            'form': form,
        }
        return render(request, 'blog/post_detail.html', context)

    def post(self, request):
        form = CommentForm(request.POST)

        if form.is_valid():
            name = request.POST['name']
            content = request.POST['content']
            comment = Comment()
            comment.name = name
            comment.content = content
            comment.save()
            return JsonResponse(model_to_dict(comment), safe=False)
        return JsonResponse({'status': 'error'}, safe=False)


class all_posts_detail(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.all()
        form = CommentForm()
        context = {
            'post': post,
            'comments': comments,
            'form': form,
        }
        return render(request, 'blog/all_posts_detail.html', context)

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            content = request.POST['content']
            comment = Comment()
            comment.name = name
            comment.content = content
            comment.save()
            return JsonResponse(model_to_dict(comment), safe=False)
        return JsonResponse({'status': 'error'}, safe=False)


@login_required(login_url='/login/')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/login/')
def index_page(request):
    logged_in_user_posts = Post.objects.filter(author=request.user).order_by('-published_date')
    post_list = logged_in_user_posts
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        logged_in_user_posts = paginator.page(page)
    except PageNotAnInteger:
        logged_in_user_posts = paginator.page(1)
    except EmptyPage:

        logged_in_user_posts = paginator.page(paginator.num_pages)
    print (logged_in_user_posts)
    return render(request, 'blog/post_list.html', {'posts': logged_in_user_posts})


@login_required(login_url='/login/')
def all_posts(request, ):
    post_list = Post.objects.all().order_by('-published_date')

    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()

    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 10)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, "blog/all_posts.html", {'posts': post_list})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('myposts')


@login_required(login_url='/login/')
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Updated")
        return redirect('myposts')

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url='/login/')
def recommendations(request):
    return render(request, 'blog/recommendations.html')