from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
  ent = util.get_entry(title)
  if ent is None:
    return render(request, "encyclopedia/error_page.html", {
      "error": "Title not found"
    })
  return render(request, "encyclopedia/entry.html", {
    "title": title,
    "body": ent
  })

