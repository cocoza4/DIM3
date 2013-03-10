
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from DIM3.settings import MEDIA_ROOT
from cocoandco.models import *


def index(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        
        template = loader.get_template('cocoandco/index.html')
        usr = request.user
        posts_list = Post.objects.filter()
        context = RequestContext(request,{ 'posts_list': posts_list, 'usr': usr })
        response = HttpResponse(template.render(context))
        return response
    return render_to_response('cocoandco/login.html', {}, context)

def category(request, category_name):
    if request.user.is_authenticated():
        context = RequestContext(request)
        template = loader.get_template('cocoandco/index.html')
        usr = request.user
        if category_name == 'new':
            posts_list = Post.objects.filter().order_by('date_time')[:10]
        else:
            posts_list = []
            list = Choice.objects.filter(category=category_name).order_by('post__date_time')[:10]
            for i in list:
                posts_list.append(i.post)
        context = RequestContext(request,{ 'usr': usr, 'posts_list': posts_list })
        response = HttpResponse(template.render(context))
        return response
    return render_to_response('cocoandco/login.html', {}, context)

def post(request, post_id_url):
    if request.user.is_authenticated():
        template = loader.get_template('cocoandco/post.html')
        username = request.user.username
        usr = User.objects.get(username=username)
        status = True
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.owner = usr
                comment.post = Post.objects.get(id=post_id_url)
                comment.save()
            else:
                status = False
        post_obj = Post.objects.get(id=post_id_url)
        comments_list = Comment.objects.filter(post=Post.objects.get(id=post_obj.id))
        commentForm = CommentForm()
        context = RequestContext(request,{ 'comments_list': comments_list, 'post_obj': post_obj,
                                              'usr': usr, 'commentForm': commentForm, 'status': status })
        response = HttpResponse(template.render(context))
        return response
    return render_to_response('cocoandco/login.html', {}, context)

def createpost(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        usr = request.user
        template = loader.get_template('cocoandco/create_post.html')
        if request.method == 'POST':
            form = PostForm(request.POST)

            if form.is_valid():
                
                post = form.save(commit=False)
                post.owner = usr
                post.like = 0
                post.rating = 0
                post.save()
                save_file(request.FILES['img'], post.id)
                for category in form.cleaned_data.get('categories'):
                    Choice(post=post, category=category).save()
                comments_list = Comment.objects.filter(post=Post.objects.get(id=post.id))
                context = RequestContext(request,{ 'comments_list': comments_list, 'post_obj': post,
                                          'usr': usr })
                template = loader.get_template('cocoandco/post.html')
                return HttpResponse(template.render(context))
            else:
                context = RequestContext(request,{ 'usr': usr, 'form': form })
                return HttpResponse(template.render(context))
        else:
            form = PostForm()
            context = RequestContext(request,{ 'usr': usr, 'form': form })
            return HttpResponse(template.render(context))
    return render_to_response('cocoandco/login.html', {}, context)

    
def save_file(file, newfilename):
    filename = file._get_name()
    fd = open('/home/cocoza4/Documents/Aptana_Studio_3_Workspace/DIM3/static/imgs/' + str(newfilename), 'wb' )
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()












