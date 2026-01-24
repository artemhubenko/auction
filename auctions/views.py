from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Lot, Bid, Comment, Category


def index(request):
    return render(request, "auctions/index.html", {
        "lots": Lot.objects.all(),
    })

@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        new_lot = Lot.objects.create(
            name=request.POST["name"],
            owner=request.user,
            description=request.POST["description"],
            category=Category.objects.get(pk=int(request.POST["category"])),
            starting_price=Decimal(request.POST["starting_price"]),
            current_bid=None,
            winner=None,
            image_url=request.POST["image_url"],
        )
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all(),
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

def lot(request, id):
    lot = Lot.objects.get(pk=int(id))
    return render(request, "auctions/lot.html", {
        "lot": lot,
        "bids": Bid.objects.filter(lot=lot).count(),
    })

@login_required(login_url='/login')
def bid(request, id):
    lot = Lot.objects.get(pk=int(id))
    amount = Decimal(request.POST["bid_amount"])
    if lot.current_bid:
        if amount <= lot.current_bid.amount:
            messages.error(request, "Your bid should be greater than the previous Bid")
            return redirect("lot", id=id)
    else: 
        if amount <= lot.starting_price:
            messages.error(request, "Your bid should be greater than the Starting price")
            return redirect("lot", id=id)

    if request.method == "POST":
        new_bid = Bid.objects.create(
            lot=Lot.objects.get(pk=int(id)),
            bidder=request.user,
            amount=amount,
        )
        lot.current_bid = new_bid
        lot.save()
        return HttpResponseRedirect(reverse('lot', args=(id, )))
    
def watchlist(request, id):
    lot = Lot.objects.get(pk=id)
    user = request.user
    if request.method == "POST":
        if lot not in user.watchlist.all():
            user.watchlist.add(lot)
        else:
            user.watchlist.remove(lot)

    return redirect("lot", id=id)