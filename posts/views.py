from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from django.utils import timezone


@login_required
def create(request):
    message = ''

    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']

        if title and url:
            Post.objects.create(
                title=title,
                url=url,
                pub_date=timezone.datetime.now(),
                author=request.user
            )
            return redirect('/')

        else:
            message = 'Please fill out the fields'

    return render(request, 'posts/create.html', {'message': message})


def home(request):
    posts = Post.objects.order_by('-votes')
    return render(request, 'posts/home.html', {'posts': posts})


def upvote(request, post_id, page='/'):
    if request.method == 'POST':
        return change_vote(request, post_id, True, page)


def downvote(request, post_id, page='/'):
    if request.method == 'POST':
        return change_vote(request, post_id, False, page)


def change_vote(request, post_id, increment, page):
    post = get_object_or_404(Post, id=post_id)
    if increment:
        post.votes += 1
    else:
        post.votes -= 1
    post.save()

    return redirect(request.META['HTTP_REFERER'])


def user_posts(request, user_id):
    posts = Post.objects.filter(author_id=user_id).order_by('-pub_date')
    username = get_object_or_404(User, id=user_id).username
    return render(request, 'posts/user.html',
                  {'posts': posts, 'username': username})
