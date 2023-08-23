from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.urls import reverse
import json
from .forms import *
from .models import *
from django.core import serializers
from django.db.models import Max
from datetime import date

today = date.today()
today_string = f"{today.year}-{today.month}-{today.day}"

def index(request):
    active_listings = Listings.objects.filter(active_state=True)
    listings = active_listings.values("title", "description", "image_link", "price", "category") 

    length_watchlist = 0
    if request.user.is_authenticated:
        watchlist_listings = Watchlist.objects.filter(user=request.user, watchlist_status=True)
        length_watchlist = len(watchlist_listings)
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist_len" : length_watchlist,
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

def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
           title = form.cleaned_data['title']
           description = form.cleaned_data['description']
           price = form.cleaned_data['price']
           image_link = form.cleaned_data['image_link']
           category = form.cleaned_data['category']
           l = Listings(user=request.user, title=title, description=description, price=price, image_link=image_link, category=category, active_state=True)
           print(l)
           l.save()
           return redirect('index')
        else:
            return HttpResponse("Failed")
    form = ListingForm()
    watchlist_listings = Watchlist.objects.filter(user=request.user, watchlist_status=True)

    return render(request, 'auctions/create.html', {
        "form": form,
        "watchlist_len": len(watchlist_listings)
    })

def show_listing(request, title):
    if request.method == 'POST':
        print(title)
        # Watchlist toggle 
        # XML Data
        data_decode = (request.body).decode("utf-8")
        data = json.loads(data_decode)
        listing_get = Listings.objects.get(title=data[1]['title'], active_state=True)
        print(data)
        if data[0] == 'watchlist':
            # get listing.model based on title

            # change watchlist status
            if data[1]['watchlistStatus'] == "Watchlisted":
                obj, created = Watchlist.objects.update_or_create(
                    user=request.user,
                    listing=listing_get,
        
                    defaults={"user": request.user, "listing": listing_get, "watchlist_status": True} 
                )
                return HttpResponse("Watchlisted")
            else:
                obj, created = Watchlist.objects.update_or_create(
                    user=request.user,
                    listing=listing_get,
        
                    defaults={"user": request.user, "listing": listing_get, "watchlist_status": False} 
                )
                return HttpResponse("Removed from watchlist")
            # Watchlist code ends
        elif data[0] == 'bid':
        #Bid logic
        
            # get bids data
            try:
                bidders = Bids.objects.filter(listing=listing_get).aggregate(Max('amount'))
            except:
                bidders = None
            if not bidders['amount__max']:
                first_bidder = Bids(user=request.user, listing=listing_get, amount=int(data[1]['bidamount']))
                update_listing_price = Listings.objects.filter(pk=listing_get.id).update(price=data[1]['bidamount'])
                first_bidder.save()   
                return redirect('goto', title=data[1]['title'])
            elif bidders['amount__max']:
                if int(data[1]['bidamount']) <= bidders['amount__max']:
                    return render(request, 'auctions/listing.html', {
                        "message": "Bid must be higher than the current highest bid."
                    })
                new_max = Bids(user=request.user, listing=listing_get, amount=data[1]['bidamount'])
                update_listing_price = Listings.objects.filter(pk=listing_get.id).update(price=data[1]['bidamount'])
                new_max.save()
                return redirect('goto', title=data[1]['title'])
        elif data[0] == 'close':
            try:
                _biddings = Bids.objects.filter(listing=listing_get).values("user", "amount")
                bidding_max = _biddings[len(_biddings) - 1]['user']
                print(bidding_max)
                highest_bid_user = User.objects.get(pk=bidding_max)
                update_listing = Listings.objects.filter(pk=listing_get.id).update(winner=highest_bid_user, active_state=False)
            except:
                update_listing = Listings.objects.filter(pk=listing_get.id).update(active_state=False)
            return redirect('index')
        elif data[0] == 'comment':
            update_comments = Comments(user=request.user, listing=listing_get, comment=data[1]['comment'], date=today_string)
            update_comments.save()
            return redirect('goto', title=data[1]['title'])

    else:
        listing_get = Listings.objects.get(title=title)
        listing = Listings.objects.filter(title=title).values("user__username", "description", "price", "image_link", "category", "active_state")
        categories = {
            "N": "No category specified",
            "F": "Fashion",
            "T": "Toys",
            "E": "Electronics",
            "H": "Home",
            "HW": "Hardware"
        }

        detail = {
            "owner": listing[0]["user__username"],
            "category": categories[listing[0]['category']]
        }
        print(detail)
        # fetch comment data if any

        comments = Comments.objects.filter(listing=listing_get).values("user__username", "comment", "date")
        comments_status = True

        # if user not logged in
        if not request.user.is_authenticated:
            return render(request, "auctions/listing.html", {
                "title": title,
                "listing": listing[0],
                "typewatchlist": "hidden",
                "typebid": "hidden",
                "typecomment": "hidden",
                "comments": comments,
                "detail": detail
            })
        # if user logged in 

        # if user owner of the listing        
        try: 
            listing_owner = Listings.objects.get(user=request.user, title=title, active_state=True)
        except:
            listing_owner = None
        if listing_owner:
            owns_listing = True
        else:
            owns_listing = False

        # if user won listing
        try:
            listing_winner = Listings.objects.get(winner=request.user, title=title, active_state=False)
        except:
            listing_winner = None
            if not listing[0]['active_state']:
                message = "This listing has been closed."
        if listing_winner:
            message = "Congrats! You've won the auction."
        elif listing[0]['active_state']:
            message = None
         # watchlist status
        try:
            watchlist = Watchlist.objects.filter(listing=listing_get, user=request.user).values("watchlist_status")
            if watchlist[0]['watchlist_status'] == True:
                watchlistStatus = 'Watchlisted'
            else:
                watchlistStatus = 'Watchlist'
        except:
            watchlistStatus = 'Watchlist'


        # bids' data
    
        try:
            biddings = Bids.objects.filter(listing=listing_get).values('user__username', 'amount')
            biddings_max = biddings.aggregate(Max('amount'))
            biddings_max['user'] = biddings[len(biddings) - 1]['user__username']
        except:
            biddings_max = {"user": "Bids so far", "amount__max": "0"}
        # bidding form
        bidding_form = BiddingForm()

        # comments form
        comment_form = CommentsForm()
   
        watchlist_listings = Watchlist.objects.filter(user=request.user, watchlist_status=True)
        
        return render(request, "auctions/listing.html", { 
            "title": title,
            "listing": listing[0],
            "watchliststatus": watchlistStatus,
            "typewatchlist": "button",
            "typebid": "button",
            "bid": biddings_max,
            "message": message,
            "bidding_form": bidding_form,
            "owns_listing": owns_listing,
            "typecomment": "button",
            "comment_form": comment_form,
            "comments": comments,
            "watchlist_len": len(watchlist_listings),
            "detail": detail
        })

def watchlist(request):
    if request.method == 'POST':
        pass
    else:
        watchlist_listings = Watchlist.objects.filter(user=request.user, watchlist_status=True)
        listings = Watchlist.objects.filter(user=request.user, watchlist_status=True).values('listing__title', 'listing__image_link', 'listing__category', 'listing__description', 'listing__price')
        print(listings)
        return render(request, 'auctions/watchlist.html',{
            "listings": listings,
            "username": request.user,
            "watchlist_len": len(watchlist_listings)
        })

def categories(request):
    if request.method == 'POST':
        pass
    else:
        watchlist_listings = Watchlist.objects.filter(user=request.user, watchlist_status=True)
        categories = [
            "Fasion",
            "Toys",
            "Electronics",
            "Home", 
            "Hardware"
        ]
        return render(request, "auctions/categories.html", {
            "categories": categories,
            "watchlist_len": len(watchlist_listings)
        }) 

def show_category(request, category):
    category_symbol = category[0]
    # if category == 'Fashion':
    #     category_symbol = 'F'
    # elif category == 'Electronics':
    #     category_symbol = 'E'
    # elif category == 'Toys':
    #     category_symbol = 'T'
    # elif category == 'Home':
    #     category_symbol = 'H'
    if category == 'Hardware':
       category_symbol = 'HW' 
    active_listings = Listings.objects.filter(category=category_symbol, active_state=True)
    listings = active_listings.values("title", "description", "image_link", "price", "category") 
    
    watchlist_listings = Watchlist.objects.filter(user=request.user, watchlist_status=True)
    
    return render(request, "auctions/category.html", {
        "categories": listings,
        "category": category,
        "watchlist_len": len(watchlist_listings)
    })