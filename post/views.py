from threading import Thread

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings

from post.models import *
from scraper.get_fb_posts_fb_page import scrapeFacebookPageFeedStatus


@login_required(login_url='/login/')
def query(request):
    queries = Query.objects.all()
    return render(request, 'query.html', {
        'queries': queries
    })


@login_required(login_url='/login/')
def post(request, query, mode):
    if query == 'all':
        posts = Post.objects.all()[:50]
    else:
        posts = Post.objects.filter(query__query=query)[:100]

    return render(request, 'post.html', {
        'posts': posts,
        'query': query,
        'mode': mode
    })


@login_required(login_url='/login/')
def post_edit(request, status_id):
    post = Post.objects.get(status_id=status_id)
    return render(request, 'post_form.html', {
        'post': post
    })

    
@login_required(login_url='/login/')
def comment(request):
    return render(request, 'query.html')


@login_required(login_url='/login/')
def retrieve_post(request):
    q = request.POST.get('q')
    if Query.objects.filter(query=q).exists():
        status = 'complete'
    else:
        query = Query.objects.create(query=q)
        # trigger search
        access_token = settings.FACEBOOK['APP_ID'] + "|" + settings.FACEBOOK['APP_SECRET']
        post_thread = Thread(target=scrapeFacebookPageFeedStatus, args=(q, access_token, query.id))
        post_thread.setDaemon(True)
        post_thread.start()

        status = 'loading'

    return JsonResponse({'status': status})


def user_login(request):
    message = ''

    if request.method == 'POST':
        next_url = request.GET.get('next', '/')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            message = 'Your login credential is not correct! Please try again.'
            
    return render(request, 'login.html', {
        'message': message,
        'l_block': 'login'
    })


def user_signup(request):
    message = ''

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.create_user(username, email, password)
            return HttpResponseRedirect('/login')
        except Exception, e:
            message = 'Your username is already used. Please try with another one!'
            
    return render(request, 'login.html', {
        'message': message,
        'l_block': 'signup'
    })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')
