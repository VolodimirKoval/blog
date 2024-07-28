from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all()
    context = {
        'title': 'Posts',
        'posts': posts,
    }
    
    return render(request, 'bloggy/list.html', context=context)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
    context = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'bloggy/detail.html', context=context)
