from django.shortcuts import render
from django.http import HttpResponse
from vjj.dec import checkLogin
from vjj.forms import suggestion
from vjj.models import Suggestion

def index(request):
    if request.method == 'POST':
         if 'suggestion' in request.POST:
             suggestion_data = request.POST['suggestion']
             name_data = request.session['name']
             suggest_model = Suggestion.objects.create(
                             name=name_data, suggestion = suggestion_data)
    
    suggest_model = Suggestion.objects.all()

    return render(request, 'index.html', {'suggestions':suggest_model})

def about(request):
    return render(request, 'about.html')

def c1(request):
    return render(request, 'contestant1.html')

def c2(request):
    return render(request, 'contestant2.html')

def s1(request):
    return render(request, 'season1.html')

def s2(request):
    return render(request, 'season2.html')

def s3(request):
    return render(request, 'season3.html')

def alls(request):
    return render(request, 'allseasons.html')

@checkLogin
def login(request, *args, **kwargs):
    return render(request, 'login.html', kwargs['data'])

@checkLogin
def suggest(request, *args, **kwargs):
    data = {
            'form' : suggestion,
            'name': kwargs['data']['name']
           }     

    return render(request, 'suggest.html', data)

def updateSession(request):
    if request.method == 'POST':
        if 'stat' in request.POST:
            if request.POST['stat'] == 'login':
                request.session['name'] = request.POST['name']
                request.session['logged_in'] = True
            elif request.POST['stat'] == 'logout':
                request.session['name'] = ''
                request.session['logged_in'] = False
    return render(request, 'index.html')
