from django.http import HttpResponse
from http import HTTPStatus
import requests
import json
from .models import Post, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from .forms import PostForm, CommentForm

# Create your views here.
def home(request):
    posts  = Post.objects.order_by('-pub_date')
    return render(request, 'posts/home.html', {'posts':posts})

def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/posts_detail.html', {'post':post})

@login_required
def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.datetime.now()
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'posts/add_comment_to_post.html', {'form': form})



@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

# Alternatives:
# def create(request):
#     if request.method == 'POST':
#         if request.POST['title'] and request.POST['url']:
#             post = Post()
#             post.title = request.POST['title']
#             post.url = request.POST['url']
#             post.body = request.POST['body']
#             if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
#                 post.url = request.POST['url']
#             else:
#                 post.url = 'http://' + request.POST['url']
#             post.pub_date = timezone.datetime.now()
#             #post.author = request.user
#             post.save()
#             return redirect('home')
#         else:
#             return render(request, 'posts/create.html', {'error':'ERROR: You must include a title and a URL to create a post.'})
#     else:
#         return render(request, 'posts/create.html')
