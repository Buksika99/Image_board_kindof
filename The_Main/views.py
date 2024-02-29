import random

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
import requests
from .forms import SearchForm, CharacterForm, CommentForm
from django.contrib.auth.decorators import user_passes_test
from .models import Character, Comment
from django.db.models import Case, When, Value, IntegerField
from django.contrib.auth import logout
from django import template
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist


def admin_required(user):
    is_admin = user.is_authenticated and user.is_staff
    print(f"User '{user.username}' is{' not' if not is_admin else ''} admin")
    return is_admin


# Create your views here.
def Welcome_Page_I_guess(request):
    return render(request, 'The_Main/index.html')


def An_Alt_Site(request):
    return HttpResponse("<title>Alt Site Title</title>Mashalla")


# Danbooru API endpoint for tags
DANBOORU_API_URL = "https://danbooru.donmai.us/posts.json"


def process_request(request, page_number, random_secluded_character):
    try:
        search_form = SearchForm(request.POST if request.method == 'POST' else None)
        rating = 'safe'

        if 'rating' in request.POST:
            rating = request.POST['rating']
            request.session['rating'] = rating  # Store the rating in session
        elif 'rating' in request.session:
            rating = request.session['rating']  # Retrieve the rating from session

        if search_form.is_valid():
            search_text = search_form.cleaned_data['searchText']
            danbooru_data = get_images(request, search_text=search_text, rating=rating)
        else:
            danbooru_data = get_images(request, rating=rating)

        secluded_data = get_default_secluded_box_images(request, page=page_number, character=random_secluded_character,
                                                        rating=rating)

        return search_form, rating, danbooru_data, secluded_data

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred in process_request: {e}")
        # Handle the error gracefully, perhaps return an appropriate response to the user
        return None, None, [], []


def index(request):
    try:
        page_number = request.GET.get('page', 1)  # Get page number from query parameters, default to 1
        random_secluded_character = random_default_secluded_box_character_chooser()
        print(f"random character chosen in index {random_secluded_character}")

        search_form, rating, danbooru_data, secluded_data = process_request(request, page_number,
                                                                            random_secluded_character)

        if search_form is None or rating is None:
            # Handle the case where there was an error processing the request
            return HttpResponseServerError("An error occurred while processing the request.")

        path = request.path
        page_name = path.rsplit('/', 1)[-1]
        character_name = page_name.replace("_", " ")

        return render(request, 'The_Main/index.html',
                      {'danbooru_data': danbooru_data, 'secluded_data': secluded_data, 'search_form': search_form,
                       'character_name': character_name.title(), 'secluded_character': random_secluded_character,
                       'ratingToggle': rating})

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred in index view: {e}")
        # Handle the error gracefully, perhaps return an appropriate response to the user
        return HttpResponseServerError("An error occurred while processing the request.")


def random_page(request, tag_name):
    try:
        page_number = request.GET.get('page', 1)  # Get page number from query parameters, default to 1
        random_secluded_character = random_default_secluded_box_character_chooser()
        print(f"random character chosen in random_page {random_secluded_character}")

        search_form, rating, danbooru_data, secluded_data = process_request(request, page_number,
                                                                            random_secluded_character)

        if search_form is None or rating is None:
            # Handle the case where there was an error processing the request
            return HttpResponseServerError("An error occurred while processing the request.")

        character_name = tag_name.replace("_", " ")

        return render(request, 'The_Main/index.html',
                      {'danbooru_data': danbooru_data, 'secluded_data': secluded_data, 'search_form': search_form,
                       'character_name': character_name.title(), 'secluded_character': random_secluded_character,
                       'ratingToggle': rating})

    except Exception as e:
        # Log the error for debugging
        print(f"An error occurred in random_page view: {e}")
        # Handle the error gracefully, perhaps return an appropriate response to the user
        return HttpResponseServerError("An error occurred while processing the request.")




def named_character_site(request, character):
    try:
        search_form = SearchForm()
        path = request.path
        page_name = path.rsplit('/', 1)[-1]
        character_name = page_name.replace("_", " ")
        pulled_objects = {}  # Initialize pulled_objects as a dictionary

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                character_obj = Character.objects.get(name=character.lower().title())
                comment.character = character_obj
                comment.user = request.user
                comment.username = request.user.username  # Save the username
                comment.save()
                # Redirect to the same page after POST to avoid form resubmission issues
                return redirect(request.path)
        else:
            comment_form = CommentForm()

        comments = Comment.objects.filter(character__name=character.lower().title())

        try:
            character = Character.objects.get(name=page_name.lower().title())
            pulled_objects['trivia'] = character.trivia
            pulled_objects['hair'] = character.hair
            pulled_objects['ability'] = character.ability
        except ObjectDoesNotExist:
            pulled_objects['trivia'] = None
            pulled_objects['hair'] = None
            pulled_objects['ability'] = None

        rating = 'safe'
        if 'rating' in request.POST:
            rating = request.POST['rating']
            request.session['rating'] = rating  # Store the rating in session
        elif 'rating' in request.session:
            rating = request.session['rating']  # Retrieve the rating from session

        character_data = get_images(request, tag_name=page_name, rating=rating)  # The side box thingie's images

        # Include pulled_objects in the dictionary passed to render
        return render(request, 'The_Main/named_character_site.html', {
            'character_data': character_data,
            'character_name': character_name.title(),
            'search_form': search_form,
            'pulled_objects': pulled_objects,
            'comment_form': comment_form,
            'comments': comments,
            'is_admin': request.user.is_staff,  # Pass whether the user is admin to the template
        })

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error in named_character_site view: {e}")
        # You can render a custom error page or redirect to a generic error page
        return HttpResponse("An error occurred. Please try again later.", status=500)



@staff_member_required
def delete_comment(request, current_path, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
        # Redirect back to the current path after deleting the comment
        return redirect(current_path)
    else:
        # Handle GET request if needed
        pass


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return index(request)
    else:
        # Handle GET request
        return index(request)


# Function to get 5 images with the "airplane" tag from Danbooru
def get_images(request, **kwargs):
    search_text = kwargs.get('search_text', None)
    tag_name = kwargs.get('tag_name', None)

    if search_text is None and 'search_text' in kwargs:
        search_text = kwargs['search_text']

    if tag_name is None and 'tag_name' in kwargs:
        tag_name = kwargs['tag_name']

    rating = ''
    print(f" THIS IS THE KWARGS GET_IMAGES: {kwargs.get('rating', 'safe')}")

    if kwargs.get('rating') == "safe":
        rating = ' rating:s -nude'
    elif kwargs.get('rating') == "disable_rating":
        rating = ' nude'

    path = request.path
    # Extract the part after the last slash to get the page name
    page_name = path.rsplit('/', 1)[-1]
    print(page_name)
    if page_name == "":
        params = {
            'tags': "airplane",
            'limit': 5
        }
    else:
        params = {
            'tags': f"{page_name}{rating}",
            'limit': 5
        }

    print(f"params {params}")

    if request.method == 'POST':
        # search_text = request.POST.get('searchText')
        params = {
            'tags': f"{search_text} rating:s -nude",
            'limit': 10
        }

    response = requests.get(DANBOORU_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return []


# Route to get the airplane images
def get_default_box_images(request, **kwargs):  # WORK ON THIS
    box_image = kwargs.get('box_image',
                           None)  # Retrieve the value of 'character' from kwargs, defaulting to None if not present

    if box_image is None:
        params = {
            'tags': "keqing",
            'limit': 1
        }
    else:
        params = {
            'tags': f"{box_image} rating:s -nude",
            'limit': 1
        }

    response = requests.get(DANBOORU_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return []


def proxy_image(request, image_url):
    # Fetch the image from the external server
    response = requests.get(image_url)

    # Return the image with appropriate content type
    content_type = response.headers['Content-Type']
    return HttpResponse(response.content, content_type=content_type)


def proxy_for_static_image(request, image_url):
    # Fetch the image from the external URL
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Set the appropriate content type for the image
        content_type = response.headers.get('content-type', 'image/jpeg, video/mp4')
        return HttpResponse(response.content, content_type=content_type)
    else:
        # If the request fails, return a placeholder image or an error message
        return HttpResponse("Image not found", status=response.status_code)


def random_default_secluded_box_character_chooser():
    character_list = ['Keqing',
                      'Raiden_Shogun',
                      'Ganyu',
                      'yelan_(genshin_impact)',
                      'kayoko_(dress)_(blue_archive)',
                      'aru_(dress)_(blue_archive)',
                      'ako_(dress)_(blue_archive)',
                      'privaty_(unkind_maid)_(nikke)',
                      'yuuka_(blue_archive)',
                      'shiroko_(blue_archive)',
                      'shiroko_terror_(blue_archive)',
                      'karin_(bunny)_(blue_archive)',
                      'asuna_(bunny)_(blue_archive)',
                      'mutsuki_(dress)_(blue_archive)',
                      'toki_(bunny)_(blue_archive)',
                      'mari_(blue_archive)',
                      'playboy_bunny']

    return random.choice(character_list)


# Function to get 5 images with the "keqing" tag from Danbooru
def get_default_secluded_box_images(request, **kwargs):
    character = kwargs.get('character',
                           'Keqing')  # Retrieve the value of 'character' from kwargs, defaulting to None if not present
    rating = ''
    print(f" THIS IS THE KWARGS SAFEONE: {kwargs.get('rating', 'safe')}")

    if kwargs.get('rating') == "safe":
        rating = ' rating:s -nude'
    elif kwargs.get('rating') == "disable_rating":
        rating = ' nude'

    page = kwargs.get('page', 1)

    params = {
        'tags': f"{character}{rating}",
        'limit': 5,
        'page': page
    }

    print(f"the parameters sent in get default {params}")

    response = requests.get(DANBOORU_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return []


# Route to get the Keqing images


def fetch_character_names(category):
    if category:
        character_names_queryset = Character.objects.filter(category=category).order_by(
            Case(
                When(order=0, then=Value(9999)),
                default='order',
                output_field=IntegerField(),
            ),
            'created_at'
        )
        return [character.name for character in character_names_queryset]
    else:
        return []


def characters(request):
    category = None

    # Determine category based on URL name
    if request.resolver_match.url_name == 'anime_characters':
        category = 'anime'
    elif request.resolver_match.url_name == 'game_characters':
        category = 'game'

    # Fetch character names based on category
    character_names = fetch_character_names(category)

    # Process character names and fetch default images
    processed_data = []
    default_images = {}
    random_secluded_character = random_default_secluded_box_character_chooser()

    for character_name in character_names:
        default_image = get_default_box_images(request, box_image=character_name)
        file_url = default_image[0].get('file_url', None) if default_image else None
        file_name = file_url if file_url else "Unknown.jpg"
        modified_name = character_name.replace('_', ' ')
        modified_name = modified_name.split('(')[0].strip().title()
        processed_data.append((character_name, modified_name, file_name))
        default_images[character_name] = file_url

    # Handle rating
    rating = 'safe'  # Default rating if not found in session
    if request.method == 'POST':
        if 'rating' in request.POST:
            rating = request.POST['rating']
            request.session['rating'] = rating  # Store the rating in session
        elif 'rating' in request.session:
            rating = request.session['rating']  # Retrieve the rating from session

    side_box_images = get_default_secluded_box_images(request, character=random_secluded_character, rating=rating)

    # Render the response based on the category
    if category == 'anime':
        anime_data = "Anime Data Here"
        return render(request, 'The_Main/characters.html',
                      {'category': category, 'side_box_images': side_box_images, 'anime_data': anime_data,
                       'character_links': processed_data, 'default_images': default_images,
                       'secluded_character': random_secluded_character, 'ratingToggle': rating})
    elif category == 'game':
        game_data = "Game Data Here"
        return render(request, 'The_Main/characters.html',
                      {'category': category, 'side_box_images': side_box_images, 'game_data': game_data,
                       'character_links': processed_data, 'default_images': default_images,
                       'secluded_character': random_secluded_character, 'ratingToggle': rating})
    else:
        # Default behavior, when the URL is just /characters/
        # You can decide what to do here, perhaps render a generic characters page
        return render(request, 'The_Main/characters.html',
                      {'side_box_images': side_box_images, 'secluded_character': random_secluded_character,
                       'ratingToggle': rating})


@user_passes_test(admin_required)
def create_character(request):
    user = request.user  # Fetch the user
    if request.method == 'POST':
        character_form = CharacterForm(request.POST)
        if character_form.is_valid():
            character_form.save()
            return redirect('index')  # Redirect to the homepage or wherever you want
    else:
        character_form = CharacterForm()

    return render(request, 'The_Main/create_character.html', {'character_form': character_form, 'user': user})


def Preview_images_for_characters(request):
    pass


def character_list_to_generate_links(request):
    character_names = ['Yukino', 'Kurisu', 'Ganyu', 'Keqing']
    return render(request, 'characters.html', {'character_names': character_names})


def get_more_images(request):
    character = request.GET.get('character', 'Keqing')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 15))

    # Assuming you have defined the DANBOORU_API_URL and the get_default_secluded_box_images function

    images = get_default_secluded_box_images(request, character=character, page=page, limit=limit)
    return JsonResponse(images, safe=False)


def default_urls():
    urls = {
        'keqing': 'https://cdn.donmai.us/sample/12/8c/__keqing_genshin_impact_drawn_by_cokecoco__sample-128cdff55cec944f4bd5af3faa176150.jpg'
                  ''
    }


register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    """
    Adds a CSS class to the form field.
    """
    return value.as_widget(attrs={'class': arg})

# https://danbooru.donmai.us/posts.json?tags=raiden_shogun&limit=1&page=1
