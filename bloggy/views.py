from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import EmailPostForm

# ----------------------------------------------------------------------------------------------------------------
# for class-based views, you also need modify urls.py in app and in list.html template
# override parameter: {% include 'includes/paginator.html' with page=posts %} to
# {% include 'includes/paginator.html' with page=page_obj %}
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'bloggy/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All posts'
        return context


# ----------------------------------------------------------------------------------------------------------------

def post_list(request):
    posts_list = Post.published.all()
    paginator = Paginator(posts_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'title': 'Posts',
        'posts': posts,
    }
    
    return render(request, 'bloggy/list.html', context=context)


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post_slug,
        status=Post.Status.PUBLISHED)
    
    context = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'bloggy/detail.html', context=context)


def post_share(request, post_id):
    post_to_share = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post_to_share.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post_to_share.title}"
            )
            message = (
                f"Read {post_to_share.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject, message=message, from_email=None, recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    
    context = {
        'title': 'Share Post',
        'post': post_to_share,
        'form': form,
        'sent': sent,
    }
    
    return render(request, 'bloggy/share.html', context=context)
