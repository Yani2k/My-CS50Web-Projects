from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new", views.create_new_page, name="create_new_page"),
    path("edit/<str:title>", views.edit_entry, name="edit_entry"),
    path("random", views.random, name="random")
]
