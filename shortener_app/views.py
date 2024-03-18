import secrets
import traceback

from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from shortener_app.forms import SignUpForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from shortener_app.models import Links
from rest_framework.response import Response
from django.db import IntegrityError

import traceback

def splash(request):
    return render(request, 'splash.html')


@login_required
def home(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            print('logged in')
            return redirect('home')
        else:
            print('user is none')
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')


def logout(request):
    '''Logout the user and redirect to the splash page'''
    user = request.user
    if user.is_authenticated:
        auth_logout(request)
    return redirect('splash')


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            hashed_pass = make_password(form.cleaned_data['password'])
            new_user = User(email=form.cleaned_data['email'], username=form.cleaned_data['email'], password=hashed_pass)
            new_user.save()
            return render(request, 'login.html')

    return render(request, 'signup.html', {'form': form})


@login_required
def manage(request):
    user = request.user
    links = Links.objects.filter(created_by=user)
    if request.method == 'POST':
        link_id = request.POST.get('link_id')
        link = Links.objects.get(id=link_id)
        link.delete()
        return redirect('manage')
    return render(request, 'manage.html', {'links': links})



def redirect_link(request, short_url):
    try:
        # Get the ShortenedURL object with the given short_url
        url = Links.objects.get(short_link=f'http://localhost:8000/{short_url}')
    except:
        return render(request, '404.html')

    # Increment the visit count
    url.visit_count += 1
    url.save(update_fields=['visit_count'])
    going_to = url.original_link
    print(f'redirecting to {going_to}')
    # Redirect to the original URL
    return redirect(going_to)


class Shorten(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)
        url = request.data['url']
        if not url:
            return Response({'error': 'URL is required'}, status=400)
        if not (url.startswith('http') or url.startswith('https')):
            url = f'http://{url}'

        # Create randomised string of 8 characters
        key = secrets.token_hex(4)
        short_url = f'http://localhost:8000/{key}'

        # Save the short URL to the database
        try:
            link = Links(original_link=url, short_link=short_url, created_by=request.user)
            link.save()
        except IntegrityError:
            return Response({'error': 'Short URL already exists'}, status=400)
        except Exception as e:
            traceback.print_exc()
            return Response({'error': 'An error occurred'}, status=400)

        return Response({'short_url': short_url}, status=200)


class Delete(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Not authenticated'}, status=401)

        link_id = request.data['id']
        try:
            link = Links.objects.get(id=link_id)
            if link.created_by != request.user:
                return Response({'error': 'Unauthorized'}, status=401)
            link.delete()
        except:
            traceback.print_exc()
            return Response({'error': 'An error occurred'}, status=400)

        return Response({'message': 'Link deleted'}, status=200)
