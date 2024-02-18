from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, SearchForm
from The_Main import views as imported_views
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse


# Create your views here.



def register(request):
    if request.method == "POST":
        registration_form = RegisterForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
    else:
        registration_form = RegisterForm()
    keqing_data = imported_views.get_images(request, tag_name="Keqing")
    return render(request, "register/register.html", {"registration_form": registration_form, 'keqing_data': keqing_data})




def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or homepage
                return redirect('/')
            else:
                return HttpResponse("Invalid username or password. Please try again.")
    else:
        login_form = AuthenticationForm()
    keqing_data = imported_views.get_images(request, tag_name="Keqing")
    return render(request, 'registration/login.html', {'login_form': login_form, 'keqing_data': keqing_data})
