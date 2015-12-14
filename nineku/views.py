from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from .models import *
from .forms import *
from .auth import *
from django.template import RequestContext
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib import auth
from django.core.context_processors import csrf
import hashlib, datetime, random




def main(request):
    if ('loginStatus' not in request.session): #initializing user session
        request.session['loginStatus'] = "notLogged"

    if request.method == 'POST': ##user logs in
        form = loginForm(request.POST)
        if form.is_valid():     ## valid input
          data = form.cleaned_data
          username = data['username']
          password = data['password']
          request.session['loginStatus'] = authUser(username,password)
          if (request.session['loginStatus'] == "invalid"):
              request.session['loginStatus'] = "notLogged"
              return render(request, 'upload/invalidLogin.html', {'loginForm':loginForm,'loginStatus':request.session['loginStatus']})

    else:
        form = loginForm()

    posts = haikuDB.objects.all()
    return render(request,'main.html', {'posts': posts, 'loginForm':form, 'loginStatus':request.session['loginStatus']})

def login(request):
    return render(request,'login.html')

def logout(request):
    request.session['loginStatus'] = "notLogged"
    return render(request,'logout.html',{'loginForm':loginForm,'loginStatus':request.session['loginStatus']})

def upload(request):
    if (request.session['loginStatus'] == "success"):
        if request.method == 'POST':
            form = haikuForm(request.POST)
            if form.is_valid():     ## valid input
              data = form.cleaned_data
              first_verseForm = data['first_verse']
              second_verseForm = data['second_verse']
              third_verseForm = data['third_verse']
              h = haikuDB(first_verse=first_verseForm, second_verse=second_verseForm, third_verse=third_verseForm)
              h.save()
              return render(request, 'upload/upload.html', {'form': form, 'loginStatus':request.session['loginStatus']})
            else:                   ##invalid input to the boxes
                return render(request, 'upload.html', {'form': ""})
    elif ( request.session['loginStatus'] == "notLogged"):
        return render(request, 'upload/loginFirst.html', {'loginForm':loginForm,'loginStatus':request.session['loginStatus']})
    elif (request.session['loginStatus'] == "inactive"):
        return render(request, 'upload/confirmFirst.html', {'loginForm':loginForm,'loginStatus':request.session['loginStatus']})
    form = haikuForm()

    return render(request, 'upload/upload.html', {'loginForm':loginForm,'form': form, 'loginStatus':request.session['loginStatus']})


def register_success(request):
    return render(request, 'registration/success.html' , {'loginForm': loginForm(), 'loginStatus':request.session['loginStatus']})

def already_confirmed(request):
    return render(request, 'registration/already_confirmed.html' , {'loginForm': loginForm(),'loginStatus':request.session['loginStatus']})

def register_user(request):
    args = {}
    args['loginStatus'] = request.session['loginStatus']
    args['loginForm'] = loginForm()
    args.update(csrf(request))
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
            48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'enyei.chan@gmail.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/success')
    else:
        args['form'] = RegistrationForm()

    return render_to_response('registration/register.html', args, context_instance=RequestContext(request))

def register_confirm(request, activation_key):
    args = {}
    args['loginStatus'] = request.session['loginStatus']
    args['loginForm'] = loginForm()
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
        request.session['loginStatus'] = "success"
        return HttpResponseRedirect('/already_confirmed')
    else: #confirm the user
        user.is_active = True

    user.save()
    request.session['loginStatus'] = "success"
    return render_to_response('registration/confirm.html', args, context_instance=RequestContext(request))
