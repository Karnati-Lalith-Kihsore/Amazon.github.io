from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.validators import RegexValidator
# Create your views here.

from django import forms
from .models import User, Listing, Cart, Buy, User_details

class User_details_form(forms.Form):
    houseno = forms.CharField()
    streetno = forms.CharField()
    village = forms.CharField()
    district = forms.CharField()
    state = forms.CharField()
    pincode = forms.IntegerField()
    phonenumber = forms.IntegerField()

class Sell_Online_form(forms.Form):
    name = forms.CharField()
    description = forms.CharField()
    price = forms.IntegerField()
    image = forms.URLField(required=False)

    name.widget.attrs.update({"class": "grid-item"})
    description.widget.attrs.update({"class": "grid-item"})
    description.widget.attrs.update({"id": "description_id"})
    price.widget.attrs.update({"class": "grid-item"})
    image.widget.attrs.update({"class": "grid-item"})

def index(request):
    return render(request, "bookstore/index.html", {
        "listings": Listing.objects.all().order_by("-timestamp")
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
            return render(request, "bookstore/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bookstore/login.html")


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
            return render(request, "bookstore/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "bookstore/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "bookstore/register.html")
    
def sell_online(request):
    if request.method == "POST":
        form = Sell_Online_form(request.POST)
        if form.is_valid():
            temp = Listing.objects.create(
                name = form.cleaned_data["name"],
                description = form.cleaned_data["description"],
                price = form.cleaned_data["price"],
                image = form.cleaned_data["image"],
                seller = request.user
            )
            temp.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "error.html", {
                "error": "Please fill the form correctly"
            })
    else:
        return render(request, "bookstore/sell_online.html", {
            "form": Sell_Online_form()
        })
    
def view_listing(request, id):
    try:
        Cart.objects.get(user=request.user, listing=Listing.objects.get(pk=id))
        message = "Remove from cart"
    except:
        message = "Add to cart"
    return render(request, "bookstore/view_listing.html", {
        "form": Listing.objects.get(pk=id),
        "cart": message
    })

def get_user_details(request, id):
    if request.method == "POST":
        temp = User_details_form(request.POST)
        if temp.is_valid():
            temp2 = User_details.objects.create(
                user = request.user,
                houseno = temp.cleaned_data["houseno"],
                streetno = temp.cleaned_data["streetno"],
                village = temp.cleaned_data["village"],
                district = temp.cleaned_data["district"],
                state = temp.cleaned_data["state"],
                pincode = temp.cleaned_data["pincode"],
                phonenumber = temp.cleaned_data["phonenumber"]
            )
            temp2.save()
            return redirect(reverse("view_listing", args=[id]))

    return render(request, "bookstore/user_details.html", {
        "form": User_details_form()
    })

def buy_listing(request, id):
    try:
        temp2 = User_details.objects.get(user=request.user)
    except:
        return redirect(reverse("get_user_details", args=[id]))
    buy = Listing.objects.get(pk=id)
    temp = Buy.objects.create(
        user = request.user,
        listing = buy
    )
    temp.save()
    return render(request, "bookstore/success.html", {
        "message": f"You have purchased the item {buy.name} successfully",
        "id": id,
        "name": buy.name
    })

def add_cart(request, id):
    temp2 = Listing.objects.get(pk=id)
    try:
        temp = Cart.objects.get(user=request.user, listing=temp2).delete()
        msg = "removed"
    except:
        temp = Cart.objects.create(
            user = request.user,
            listing = temp2
        )
        temp.save()
        msg = "added"
    return render(request, "bookstore/success.html", {
        "message": f"You have {msg} the item \"{temp2.name}\" successfully",
        "id": id,
        "name": temp2.name
})

def notification(request):
    try:
        temp = Buy.objects.filter(listing=Listing.objects.filter(user=request.user))
        address = []
        for i in temp:
            temp2 = User_details.objects.get(user=i.user)
            address.append(temp2)
        length = len(temp)
        return render(request, "bookstore/notification.html", {
            "forms": temp,
            "address": address,
            "length": length
        })
    except:
        return render(request, "bookstore/notification.html", {
            "message": "You have no notifications currently"
        })