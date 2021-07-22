from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, NewUserForm
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

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
