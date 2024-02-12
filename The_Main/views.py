from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import requests
from .forms import SearchForm


# Create your views here.
def Welcome_Page_I_guess(request):
    return render(request, 'The_Main/index.html')


def An_Alt_Site(request):
    return HttpResponse("<title>Alt Site Title</title>Mashalla")


# Danbooru API endpoint for tags
DANBOORU_API_URL = "https://danbooru.donmai.us/posts.json"


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_text = form.cleaned_data['searchText']
            danbooru_data = get_default_images(request, search_text)
            keqing_data = get_keqing_images(request)
        else:
            danbooru_data = get_default_images(request)
            keqing_data = get_keqing_images(request)
    else:
        form = SearchForm()
        danbooru_data = get_default_images(request)
        keqing_data = get_keqing_images(request)

    return render(request, 'The_Main/index.html',
                  {'danbooru_data': danbooru_data, 'keqing_data': keqing_data, 'form': form})


# Function to get 5 images with the "airplane" tag from Danbooru
def get_default_images(request, *args):
    if args:  # Check if args is not empty
        search_text = args[0]  # Assign the first argument to search_text
        # Now you can use search_text in your function
    else:
        search_text = None

    params = {
        'tags': "airplane",
        'limit': 5
    }
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
def default_images():
    images = get_default_images()
    return JsonResponse(images, safe=False)


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


# Function to get 5 images with the "keqing" tag from Danbooru
def get_keqing_images(request):
    params = {
        'tags': "keqing",
        'limit': 5
    }

    response = requests.get(DANBOORU_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return []


# Route to get the Keqing images
def keqing_images(request):
    images = get_keqing_images()
    return JsonResponse(images, safe=False)
