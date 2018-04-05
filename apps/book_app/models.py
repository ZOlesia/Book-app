from __future__ import unicode_literals
from django.db import models
# import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class BlogManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or not postData['first_name'].isalpha():
            errors['first_name'] = "First name should be more than 2 characters and letters only"
        if len(postData['last_name']) < 2 or not postData['last_name'].isalpha():
            errors['last_name'] = "Last name should be more than 2 characters and letters only"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email1'] = "Not valid email"
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['email2'] = "Email already exists"
        if len(postData['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters in length"
        if postData['confirm'] != postData['password']:
            errors['confirm'] = "Password doesn`t match"
        return errors

    def login_validator(self, postData):
        errors = {}
        # hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        if len(postData['email']) < 1:
            errors['log_email1'] = 'Email field is empty'
        if len(User.objects.filter(email = postData['email'])) == 0 :
            errors['log_email2'] = 'Please check your email otherwie go to register'
        # if bcrypt.checkpw(postData['password'].encode(), hash1.encode()):
        #     errors['log_password'] = "Password doesn`t match"
        if len(User.objects.filter(password = postData['password'])) == 0 :
            errors['log_email2'] = 'Password is incorrect'
        return errors


# class BookManager(models.Manager):
#     def create_validator(self, postData):
#         errors = {}
#         if not len(postData['new_author']):
#             auth = postData['choose_author']
#         else:
#             auth = postData['new_author']

#         if len(Author.objects.fiter(name = auth)) > 0:
#             errors['author'] = "Author already exists, please choose from the following authors"
#         return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    conf_password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Author(models.Model):
    name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = BookManager()

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.ForeignKey(Author, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    content = models.TextField()
    rating = models.CharField(max_length = 1)
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviewers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


