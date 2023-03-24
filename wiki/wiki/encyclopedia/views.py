from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from random import choice

from . import util


def index(request):
  return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
  })
    
def entry(request, title):
  if request.method == "POST":
    return HttpResponseRedirect(reverse("edit_entry", kwargs={
      "title": title
    }))
  ent = util.get_entry(title)
  if ent is None:
    return render(request, "encyclopedia/error_page.html", {
      "error": "Title not found"
    })
  return render(request, "encyclopedia/entry.html", {
    "title": title,
    "body": markdown2.markdown(ent)
  })

def search(request):
  title = request.GET.get("q", "").lower()
  if title == "":
    return render(request, "encyclopedia/error_page.html", {
      "error": "No input to the search"
    }) 
  ent = util.get_entry(title)
  if ent is not None:
    return HttpResponseRedirect(reverse("entry", kwargs={
      "title": title
      }))
  else:
    all_ent = util.list_entries()
    matching = [s for s in all_ent if title in s.lower()]
    return render(request, "encyclopedia/index.html", {
      "entries": matching
    })
    
def create_new_page(request):
  if request.method == "POST":
    title = request.POST["title"]

    if util.get_entry(title) is not None:
      return render(request, "encyclopedia/error_page.html", {
        "error": "An entry with such a title already exists."
      })
    
    content = request.POST["content"]
    util.save_entry(title, content)
    return HttpResponseRedirect(reverse("index"))
    
  return render(request, "encyclopedia/create_new_page.html")

def edit_entry(request, title):
  if request.method == "POST":
    content = request.POST["content"]
    util.save_entry(title, content)
    return HttpResponseRedirect(reverse("entry", kwargs={
      "title": title
    }))
  ent = util.get_entry(title)
  if ent is None:
    render(request, "encyclopedia/error_page.html", {
      "error": "No such entry available to be editted."
    })
  return render(request, "encyclopedia/edit_entry.html", {
    "content": ent,
    "title": title
  })
    
def random(request):
  entries = util.list_entries()
  selected_entry = choice(entries)
  return HttpResponseRedirect(reverse("entry", kwargs={
    "title": selected_entry
  }))