from django.contrib import admin
from .models import Movie, Category, Cast, Director, Author


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "rate", "release_year"]
    list_per_page = 20
    search_fields = ["title", "summary"]
    list_filter = ["release_year"]


# Register your models here.
@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 20
    search_fields = ["name"]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 20
    search_fields = ["name"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 20
    search_fields = ["name"]


@admin.register(Category)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "type"]
    list_per_page = 20
    search_fields = ["title", "type"]
