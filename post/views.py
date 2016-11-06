from threading import Thread

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings

from post.models import *
from scraper.get_fb_posts_fb_page import scrapeFacebookPageFeedStatus
from scraper.get_fb_comments_from_fb import scrapeFacebookPageFeedComments
from allauth.socialaccount.models import *


@login_required(login_url='/login/')
def query(request):
    user = ",{},".format(request.user.id)
    queries = Query.objects.filter(users__contains=user)
    return render(request, 'query.html', {
        'queries': queries
    })


@login_required(login_url='/login/')
def post(request, query, mode):
    if query == 'all':
        user = ",{},".format(request.user.id)
        queries = Query.objects.filter(users__contains=user)
        posts = Post.objects.filter(query__in=queries)[:200]
    else:
        posts = Post.objects.filter(query__query=query)[:200]

    return render(request, 'post.html', {
        'posts': posts,
        'query': query,
        'mode': mode
    })


@login_required(login_url='/login/')
def comment(request, post_id, mode):
    comments = Comment.objects.filter(post_id=post_id)[:200]
    return render(request, 'comment.html', {
        'comments': comments,
        'mode': mode,
        'post_id': post_id
    })


@login_required(login_url='/login/')
def post_edit(request, status_id):
    post = Post.objects.get(status_id=status_id)
    return render(request, 'post_form.html', {
        'post': post
    })


@login_required(login_url='/login/')
def comment_edit(request, comment_id):
    comment = Comment.objects.get(comment_id=comment_id)
    return render(request, 'comment_form.html', {
        'comment': comment
    })


@login_required(login_url='/login/')
def blog(request, slug):
    blog = Blog.objects.get(url=slug)
    return render(request, 'blog.html', {
        'blog': blog
    })


@login_required(login_url='/login/')
def facebook(request):
    try:
        facebook_data = SocialAccount.objects.get(user=request.user, 
            provider='facebook').extra_data

        accounts = [{
            'name': facebook_data['name'], 
            'id': facebook_data['id'],
            'primary': 'Primary Account' 
        }]

        for item in facebook_data['context']['mutual_likes']['data']:
            account = {'name': item['name'], 'id': item['id']}
            accounts.append(account)
    except Exception, e:
        accounts = []

    return render(request, 'facebook_accounts.html', {'accounts': accounts})


@login_required(login_url='/login/')
def retrieve_post(request):
    q = request.POST.get('q')
    user = ",{},".format(request.user.id)
    query = Query.objects.filter(query=q).first()
    if query:
        status = 'complete'
        # register the user to this query
        if query.users:
            query.users = query.users + user
        else:
            query.users = user
            
        query.save()
    else:
        query = Query.objects.create(query=q, users=user)
        # trigger search
        access_token = settings.FACEBOOK['APP_ID'] + "|" + settings.FACEBOOK['APP_SECRET']
        post_thread = Thread(target=scrapeFacebookPageFeedStatus, args=(q, access_token, query.id))
        post_thread.setDaemon(True)
        post_thread.start()

        status = 'loading'

    return JsonResponse({'status': status})


@login_required(login_url='/login/')
def retrieve_comment(request):
    post_id = request.POST.get('post_id')
    if Comment.objects.filter(post_id=post_id).exists():
        status = 'complete'
    else:
        # trigger search
        access_token = settings.FACEBOOK['APP_ID'] + "|" + settings.FACEBOOK['APP_SECRET']
        post_thread = Thread(target=scrapeFacebookPageFeedComments, args=(access_token, post_id))
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
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
        except Exception, e:
            print e
            message = 'Your username is already used. Please try with another one!'
            
    return render(request, 'login.html', {
        'message': message,
        'l_block': 'signup'
    })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')
