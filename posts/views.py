from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post

# Create your views here.


@login_required
def create(req):
    if req.method == 'POST':
        if req.POST['title'] and req.POST['url']:
            post = Post()
            post.title = req.POST['title']
            if req.POST['url'].startswith('http://') or req.POST['url'].startswith('https://'):
                post.url = req.POST['url']
            else:
                post.url = 'http://' + req.POST['url']
            post.pub_date = timezone.datetime.now()
            post.author = req.user
            post.save()
            return redirect('home')
        else:
            return render(req, 'posts/create.html', {'error': 'ERROR: You must include a title and URL'})
    else:
        return render(req, 'posts/create.html')


def home(req):
    posts = Post.objects.order_by('-votes_total')
    return render(req, 'posts/home.html', {'posts': posts})


def upvote(req, pk):
    post = Post.objects.get(pk=pk)
    post.votes_total += 1
    post.save()
    return redirect('home')


def downvote(req, pk):
    post = Post.objects.get(pk=pk)
    post.votes_total -= 1
    post.save()
    return redirect('home')
