
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.contrib.auth.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import auth

from DIM3.settings import MEDIA_ROOT
from cocoandco.models import *

#def getPicURL(post_id):
#    file_exists = False
#    for filename in os.listdir('/home/cocoza4/Documents/Aptana_Studio_3_Workspace/DIM3/static/imgs/'):
#        if filename.startswith(str(post_id)):
#            file_exists = True
#            url = str(post_id) + '.' + filename.split('.')[-1].lower()
#            break 
#    if not file_exists:
#        url = 'no-image.jpg'
#    return url

def login(request):
    username = request.POST['username']
    passwd = request.POST['passwd']
    usr = auth.authenticate(username = username, password = passwd)
    if usr is not None and usr.is_active:
        auth.login(request, usr)
    return HttpResponseRedirect('/')

def register(request):
    template = loader.get_template('cocoandco/register.html')
    if request.method == 'POST':
        
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            name = request.POST['name']
            surname = request.POST['lastname']
            email = request.POST['email']
            username = request.POST['username']
            passwd = request.POST['password']
            passwd = make_password(passwd)
            usr = User.objects.create(username = username, password = passwd, first_name = name, 
                                       last_name = surname, email = email)
            usr = auth.authenticate(username = username, password = request.POST['password'])
            member = form.save(commit=False)
            member.usr = usr
            member.save()
            if 'img' in request.FILES:
                save_file(request.FILES['img'], member.id, '/home/cocoza4/Documents/Aptana_Studio_3_Workspace/DIM3/static/imgs/display_imgs/')
                filename = str(request.FILES['img'])
                ext = filename.split('.')[-1].lower()
                member.img = str(member.id) + '.' + ext
            else:
                member.img = 'anonymous.png'
            member.save()
            return HttpResponseRedirect('/')
        else:
            context = RequestContext(request,{ 'registrationForm': form})
            return HttpResponse(template.render(context))            
    else:
        form = RegistrationForm()
        context = RequestContext(request,{'registrationForm': form })
        return HttpResponse(template.render(context))
        
def user(request, user_id_url):
    context = RequestContext(request)
    if request.user.is_authenticated():
        usr = Member.objects.get(usr__username=request.user.username)
    else:
        usr = None
    template = loader.get_template('cocoandco/user.html')

def index(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        usr = Member.objects.get(usr__username=request.user.username)
    else:
        usr = None
    template = loader.get_template('cocoandco/index.html')
    keyword = ''
    posts_list = []
    if request.GET.get('search'):
        cats = request.GET.getlist('cat')[0]
        keyword = request.GET['search']
        for cat in cats.split(','):
            list = Choice.objects.distinct().filter(category=cat).values_list('id')
            entries = Choice.objects.filter((Q(id__in=list) & Q(post__title__icontains=keyword)) | 
                                           (Q(id__in=list) & Q(post__description__icontains=keyword)))
            for i in entries:
                posts_list.append(i.post)
    else:
        
        if request.GET.getlist('cat') == []:
            posts_list = Post.objects.filter()
        else:
            cats = request.GET.getlist('cat')[0]
            print cats
            for cat in cats.split(','):
                list = Choice.objects.distinct().filter(category=cat).values_list('id')
                entries = Choice.objects.filter(Q(id__in=list))
            for i in entries:
                posts_list.append(i.post)
    context = RequestContext(request,{ 'posts_list': posts_list, 'usr': usr })
    return HttpResponse(template.render(context))


def category(request, category_name):
    if request.user.is_authenticated():
        usr = Member.objects.get(usr__username=request.user.username)
    else:
        usr = None

    context = RequestContext(request)
    template = loader.get_template('cocoandco/index.html')
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

def post(request, post_id_url):
    if request.user.is_authenticated():
#        usr = request.user
        usr = Member.objects.get(usr__username=request.user.username)
    else:
        usr = None
    template = loader.get_template('cocoandco/post.html')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = usr
            comment.post = Post.objects.get(id=post_id_url)
            comment.save()
            return HttpResponseRedirect('/post/%i/' % comment.post.id)
    post_obj = Post.objects.get(id=post_id_url)

    comments_list = Comment.objects.filter(post=Post.objects.get(id=post_obj.id))
    commentForm = CommentForm()
    context = RequestContext(request,{ 'comments_list': comments_list, 'post_obj': post_obj,
                                          'usr': usr, 'commentForm': commentForm})
#    return HttpResponse(template.render(context))
    return render_to_response('cocoandco/post.html', { 'comments_list': comments_list, 'post_obj': post_obj,
                                          'usr': usr, 'commentForm': commentForm}, context) 

def createpost(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        template = loader.get_template('cocoandco/create_post.html')
#        usr = request.user
        usr = Member.objects.get(usr__username=request.user.username)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                
                post = form.save(commit=False)
                post.owner = usr
                post.like = 0
                post.rating = 0
                post.save()
                if 'img' in request.FILES:
                    save_file(request.FILES['img'], post.id, '/home/cocoza4/Documents/Aptana_Studio_3_Workspace/DIM3/static/imgs/')
                    filename = str(request.FILES['img'])
                    ext = filename.split('.')[-1].lower()
                    post.img = str(post.id) + '.' + ext
                else:
                    post.img = 'no-image.jpg'
                post.save()
                
    
                for category in form.cleaned_data.get('categories'):
                    Choice(post=post, category=category).save()
    
                return HttpResponseRedirect('/post/%i/' % post.id)
            else:
                context = RequestContext(request,{ 'usr': usr, 'form': form })
                return HttpResponse(template.render(context))
        else:
            form = PostForm()
            context = RequestContext(request,{ 'usr': usr, 'form': form })
            return HttpResponse(template.render(context))
    return HttpResponseRedirect('/')
    
def save_file(file, newfilename, path=''):
    ext = str(file).split('.')[-1].lower()
    filename = file._get_name()
    
    fd = open(path + str(newfilename) + '.' + ext, 'wb' )
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()












