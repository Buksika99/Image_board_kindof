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

    # Call process_request function to get required data
    page_number = request.GET.get('page', 1)  # Get page number from query parameters, default to 1
    random_secluded_character = imported_views.random_default_secluded_box_character_chooser()
    search_form, rating, danbooru_data, secluded_data = imported_views.process_request(request, page_number, random_secluded_character)

    # Additional data retrieval
    character_name = "Keqing"  # Example tag name
    keqing_data = imported_views.get_images(request, tag_name=character_name)

    # Render the template with the retrieved data
    return render(request, "register/register.html", {
        "registration_form": registration_form,
        "danbooru_data": danbooru_data,
        "secluded_data": secluded_data,
        "search_form": search_form,
        "character_name": character_name.title(),
        "secluded_character": random_secluded_character,
        "ratingToggle": rating,
        "keqing_data": keqing_data
    })


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

    # Call process_request function to get required data
    page_number = request.GET.get('page', 1)  # Get page number from query parameters, default to 1
    random_secluded_character = imported_views.random_default_secluded_box_character_chooser()
    search_form, rating, danbooru_data, secluded_data = imported_views.process_request(request, page_number, random_secluded_character)

    # Additional data retrieval
    character_name = "Keqing"  # Example tag name
    keqing_data = imported_views.get_images(request, tag_name=character_name)

    # Render the template with the retrieved data
    return render(request, 'registration/login.html', {
        'login_form': login_form,
        'danbooru_data': danbooru_data,
        'secluded_data': secluded_data,
        'search_form': search_form,
        'character_name': character_name.title(),
        'secluded_character': random_secluded_character,
        'ratingToggle': rating,
        'keqing_data': keqing_data
    })