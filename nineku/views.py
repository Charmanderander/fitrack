from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from .models import *
from .forms import *
from .auth import *
from .search import *
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.http import JsonResponse
from django.db.models import Count
from django.template.defaulttags import register
import hashlib, datetime, random

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def likeProcess(request):
    if request.method == 'POST':
        postid = request.POST.get('id')
        username = request.POST.get('username')
        if(Likes.objects.filter(user=username, postid=postid).exists()):
            deleteLike = Likes.objects.filter(user=username, postid=postid)
            deleteLike.delete()
        else:
            saveLike = Likes(user=username, postid=postid)
            saveLike.save()
        return JsonResponse({'foo':'bar'})
    else:
        return JsonResponse({'foo':'bar'})

def generateLikeList(request):
    username = request.session['username']
    likes = Likes.objects.all().filter(user=username)
    likesPerPost = Likes.objects.values('postid').annotate(num_likes=Count('postid'))

    userl = []
    postl = []

    print("hello")
    print(len(likes))
    print("hello")
    for like in likes:
        userl.append(like.user)
        postl.append(like.postid)

    likeDict = {}
    print(likesPerPost)
    for likedPosts in likesPerPost:
        likeDict[likedPosts['postid']] = likedPosts['num_likes']

    print(likeDict)

    return userl, postl, likeDict

def myAdminPage(request):
    if ('loginStatus' not in request.session): #initializing user session
        request.session['loginStatus'] = "notLogged"
    if ('username' not in request.session): #initializing user session
        request.session['username'] = "notLogged"

    [userl, postl, likeDict] = generateLikeList(request)

    posts = dreamDB.objects.order_by('-pk').all()

    return render(request,'adminPage.html', {'likeDict':likeDict, 'userl':userl, 'postl':postl, 'posts': posts, 'loginForm':loginForm, 'loginStatus':request.session['loginStatus'],'username':request.session['username']})


def main(request):
    if ('loginStatus' not in request.session): #initializing user session
        request.session['loginStatus'] = "notLogged"
    if ('username' not in request.session): #initializing user session
        request.session['username'] = "notLogged"

    [userl, postl, likeDict] = generateLikeList(request)

    posts = dreamDB.objects.order_by('-pk').all()

    return render(request,'main.html', {'likeDict':likeDict, 'userl':userl, 'postl':postl, 'posts': posts, 'loginForm':loginForm, 'loginStatus':request.session['loginStatus'],'username':request.session['username']})

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():     ## valid input
          data = form.cleaned_data
          username = data['username']
          password = data['password']
          request.session['loginStatus'] = authUser(username,password)
          if (request.session['loginStatus'] == "success" or request.session['loginStatus'] == "inactive"):
              request.session['username'] = username
          elif (request.session['loginStatus'] == "invalid"):
              request.session['loginStatus'] = "notLogged"
              return render(request, 'upload/invalidLogin.html', {'loginForm':loginForm,'loginStatus':request.session['loginStatus']})
    return HttpResponseRedirect("/")

def logout(request):
    request.session.flush()
    request.session['loginStatus'] = "notLogged"
    request.session['username'] = "notLogged"
    return render(request,'logout.html',{'loginForm':loginForm,'loginStatus':request.session['loginStatus']})

def register_success(request):
    return render(request, 'registration/success.html' , {'loginForm': loginForm(), 'loginStatus':request.session['loginStatus']})

def already_confirmed(request):
    return render(request, 'registration/already_confirmed.html' , {'loginForm': loginForm(),'loginStatus':request.session['loginStatus']})


def upload(request):
    if (request.session['loginStatus'] == "success"):
        if request.method == 'POST':
            form = runForm(request.POST)
            if form.is_valid():     ## valid input
              data = form.cleaned_data
              title = data['title']
              distance = data['distance']
              duration = data['duration']
              time = data['time']
              location = data['location']
              description = data['description']
              username = request.session['username']
              h = dreamDB(title=title, distance=distance, duration=duration, time=time, location=location, description=description, user=username)
              h.save()
              return HttpResponseRedirect("/")
            else:                   ##invalid input to the boxes
                return render(request, 'upload.html', {'form': ""})
    elif ( request.session['loginStatus'] == "notLogged"):
        return render(request, 'upload/loginFirst.html', {'loginForm':loginForm,'loginStatus':request.session['loginStatus']})
    elif (request.session['loginStatus'] == "inactive"):
        return render(request, 'upload/confirmFirst.html', {'loginForm':loginForm,'loginStatus':request.session['loginStatus'],'username':request.session['username']})
    form = runForm()

    return render(request, 'upload/upload.html', {'loginForm':loginForm,'form':form, 'loginStatus':request.session['loginStatus'],'username':request.session['username']})

@csrf_protect
def register_user(request):
    args = {}
    args['loginStatus'] = request.session['loginStatus']
    args['loginForm'] = loginForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            activation_key = hashlib.sha1((salt+email).encode('utf-8')).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Get user by username
            user=User.objects.get(username=username)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours www.dreamrlog.com/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'dreamrlog@gmail.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/success')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))

def register_confirm(request, activation_key):
    args = {}
    args['loginStatus'] = "notLogged"
    args['loginForm'] = loginForm()
    args['username'] = "notLogged"
    #check if user is already logged in and if he is, redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        return render_to_response('registration/confirm_expired.html', args, context_instance=RequestContext(request))
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user

    if (user.is_active == True): #User already confirmed
        return HttpResponseRedirect('/already_confirmed')
    else: #confirm the user
        user.is_active = True

    user.save()
    return render_to_response('registration/confirm.html', args, context_instance=RequestContext(request))

def viewUserPosts(request):
    username = request.session['username']
    posts = dreamDB.objects.order_by('-pk').all().filter(user=username)

    if request.method == 'POST' and 'likepost' in request.POST:
        likeProcess(request)

    [userl, postl, likeDict] = generateLikeList(request)

    return render(request,'viewUserPosts.html', {'likeDict':likeDict, 'userl':userl,'postl':postl,'userPosts': posts, 'loginForm':loginForm(), 'loginStatus':request.session['loginStatus'],'username':request.session['username'],'viewUserPosts':1})

def search(request):
    query_string = ''
    found_entries = None
    if ('search' in request.GET) and request.GET['search'].strip():
        query_string = request.GET['search']
        entry_query = get_query(query_string, ['title', 'distance', 'duration', 'description', 'time', 'location', 'user'])
        found_entries = dreamDB.objects.order_by('-pk').filter(entry_query)

    if request.method == 'POST' and 'likepost' in request.POST:
        likeProcess(request)

    [userl, postl, likeDict] = generateLikeList(request)

    return render(request,'search/searchResults.html', {'likeDict':likeDict, 'userl':userl,'postl':postl,'query_string': query_string, 'found_entries': found_entries, 'loginForm':loginForm(), 'loginStatus':request.session['loginStatus'],'username':request.session['username']})
