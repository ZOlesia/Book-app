# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'book_app/index.html')
def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(index)
    else:
        new_user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'], 
            email = request.POST['email'], 
            password = request.POST['password'], 
            conf_password = request.POST['confirm']
        )
        request.session['user_id'] = new_user.id
        return redirect(home)
        
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect(index)
    else:
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id

        return redirect(home)

def logout(request):
    request.session.clear()
    return redirect('/')


def home(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context =  {
        'user': User.objects.get(id = request.session['user_id']),
        'last_reviews': Review.objects.all()[len(Review.objects.all()) - 3:],
        'all_reviews': Review.objects.all()   
    }
    return render(request, 'book_app/home.html', context)

def add(request):
    return render(request, 'book_app/new_book.html', {'all_author': Author.objects.all() })

def create(request):
    if not len(request.POST['new_author']):
        auth = request.POST['choose_author']
    else:
        auth = request.POST['new_author']
    existing_auth = Author.objects.filter(name = auth)
    if len(existing_auth) > 0:
        new_auth = Author.objects.filter(name = auth)[0]
    else:
        new_auth = Author.objects.create(name = auth)
    
    new_book = Book.objects.create(
        title = request.POST['title'],
        author = new_auth
    )
    request.session['newly_created_book'] = new_book.id
    print request.session['newly_created_book']
    
    current_user = User.objects.get(id=request.session['user_id'])
    new_review = Review.objects.create(
        content =  request.POST['review'],
        rating =  request.POST['rating'],
        book = new_book,
        user = current_user
    )
    redir_str = '/books/' + str(request.session['newly_created_book'])
    return redirect(redir_str)

def book(request, id):
    context = {
        'book': Book.objects.get(id = id),
        'all_reviews': Review.objects.all().filter(book = Book.objects.get(id = id))
    }
    return render(request, 'book_app/book.html', context)

def proccess(request, id):
    current_user = User.objects.get(id=request.session['user_id'])
    Review.objects.create(
        content = request.POST['add_review'],
        rating = request.POST['rating'],
        book = Book.objects.get(id = id),
        user = current_user
    )
    return redirect('/books/' + str(id))

def user(request, id):
    context = {
        'user': User.objects.get(id=id),
        'reviews': Review.objects.filter(user = id)
    }
    request.session['count'] = len(Review.objects.filter(user = id))
    return render(request, 'book_app/user.html', context)