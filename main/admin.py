from django.contrib import admin
from .models import Movie, Category, Artist


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "rate", "release_year"]
    list_per_page = 20
    search_fields = ["title", "summary"]
    list_filter = ["release_year"]


# Register your models here.
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 20
    search_fields = ["name"]


@admin.register(Category)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "type"]
    list_per_page = 20
    search_fields = ["title", "type"]
