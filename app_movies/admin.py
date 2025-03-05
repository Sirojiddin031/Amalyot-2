from django.contrib import admin

from app_movies.models import Movie, Actor, Comment

admin.site.register([Movie,Actor,Comment])
