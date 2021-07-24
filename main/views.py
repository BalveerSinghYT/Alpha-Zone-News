from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewUserForm
from django.http import HttpResponse
from django.contrib import messages
import requests
import QuickNews.settings
from .forms import *
# Create your views here.

APIKEY = 'f43c5eef8c544690bbcd43d4a58ebfb3'

def home(request):
    context = {'blogs' : BlogModel.objects.all()}
    return render(request , 'home.html' , context)



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


def add_blog(request):
    context = {'form' : BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image
            )
            print(blog_obj)
            return redirect('/')
            
            
    
    except Exception as e :
        print(e)
    
    return render(request , 'add_blog.html' , context)

def see_blog(request):
    context = {}
    
    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] =  blog_objs
    except Exception as e: 
        print(e)
    
    print(context)
    return render(request , 'see_blog.html' ,context)

def blog_detail(request , slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] =  blog_obj
    except Exception as e:
        print(e)
    return render(request , 'blog_detail.html' , context)


def blog_update(request , slug):
    context = {}
    try:
        
        
        blog_obj = BlogModel.objects.get(slug = slug)
       
        
        if blog_obj.user != request.user:
            return redirect('/')
        
        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial = initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']
            
            blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image
            )
        
        
        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e :
        print(e)

    return render(request , 'update_blog.html' , context)

def blog_delete(request , id):
    try:
        blog_obj = BlogModel.objects.get(id = id)
        
        if blog_obj.user == request.user:
            blog_obj.delete()
        
    except Exception as e :
        print(e)

    return redirect('/see-blog')
