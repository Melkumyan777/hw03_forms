from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import redirect
from .forms import PostForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Group, User
from .models import Post


User = get_user_model()



def index(request):
    posts = Post.objects.all()[:10]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "posts": posts,
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    posts = Post.objects.all()[:10]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "posts": posts,
        'page_obj': page_obj,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    posts_count = posts.count()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts_count': posts_count,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            username = form.author
            return redirect(f'/profile/{username}/') 
        return render(request, 'posts/create_post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'posts/create_post.html', {'form': form} )


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form = form.save(commit=False)
                form.author_id = request.user.id
                form.save()
                return redirect(f'/posts/{post.id}/')
            context = {
                'form': form,
                'is_edit': is_edit,}
            return render(request, 'post_edit', context)
        else:
            form = PostForm(instance=post)
            context = {
                'form': form,
                'is_edit': is_edit,}
            return render(request, 'posts/create_post.html', context)
    return redirect('index')