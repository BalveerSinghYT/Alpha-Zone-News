from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewUserForm
from django.http import HttpResponse
from django.contrib import messages
import requests
import QuickNews.settings
# Create your views here.

APIKEY = 'f43c5eef8c544690bbcd43d4a58ebfb3'

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])

            if user is not None:
                login(request, user)
                return HttpResponse('Authentication was successfull')

            else:
                return HttpResponse('Authentication failed, please try again.')
    
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form':form})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form})

def news(request):
    url = f'https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={APIKEY}'
    response = requests.get(url)
    data = response.json()
    # print(data)
    articles = data['articles']
    # print(articles)

    context = {
        'articles' : articles
    }

    return render(request, 'news.html', context)
