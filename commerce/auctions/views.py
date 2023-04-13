from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Listing_Category, Listing


def index(request):
    return render(request, "auctions/index.html", {
      "active_listings" : Listing.objects.filter(buyer=None)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def add(request):
  if request.method == "POST":
    title = request.POST["title"]
    min_bid = request.POST["min_bid"]
    close_date = request.POST["close_date"]
    photo = request.POST["photo"]
    description = request.POST["description"]
    category = Listing_Category.objects.get(category_name=request.POST["category"])
    seller = request.user
    new_listing = Listing(seller=seller, category=category, minimal_bid=min_bid, closing_date=close_date, photo=photo, title=title, description=description)
    new_listing.save()
  return render(request, "auctions/add_listing.html", {
    "categories": Listing_Category.objects.all()
  })
  
  
def listing(request, listing_id):
  try:
    listing = Listing.objects.get(pk=listing_id)
  except:
    return render(request, "auctions/error_page.html", {
      "error_message": "No such listing exists!"
    })
    
  return render(request, "auctions/listing.html", {
    "listing": listing
  })
  