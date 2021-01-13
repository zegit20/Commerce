from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import User,auction,category,bid,comment,activelisting


comments_on_auction = []
bids_on_auction =[]
message1 = ""

def index(request):
    return render(request, "auctions/index.html",{
          "auctions":auction.objects.all() 
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

def create_view(request):
    global comments_on_auction
    print("second check")
    # categories = category.objects.all()
    
    # print (categories)
    if request.method == "POST" : 
        print("first check")
        bid = request.POST['bid']
        title = request.POST['Title']
        url = request.POST['Image']
        description0 = request.POST['Description']
        category0 = category.objects.get(pk=int(request.POST["category"]))
        print (title)
        print(bid)
        print(url)
        print( description0)
        print(request.user.id)
        auction0 = auction(title = title , starting_bid = bid, image_url = url , category = category0,  is_active = True, created_by = request.user , created_on=  datetime.datetime.now(), description = description0 )
        print(auction0)
        auction0.save()
        comments = comment.objects.all()
       
        # activelisting0 = activelisting.objects.get(pk=1)
        # print(activelisting0)
        return render(request, "auctions/index.html",{
          "auctions":auction.objects.all()  
        })
            
    print("heloo")    
    return  render(request, "auctions/create.html")

def visit_item(request, auction_id):
    global bids_on_auction
    global comments_on_auction
    global message1
    item = auction.objects.get(pk=int(auction_id))
    watcher0 =request.user
    activelisting0 = activelisting.objects.get(watcher=watcher0)
    actives = activelisting0.active.all()
    if item in actives:      
        value = "Remove-Item"
    else:    
        value = "Add-Item"
    print(item)
    show_items(request, auction_id)
    return render(request, "auctions/item.html",{
        "item":auction.objects.get(pk=int(auction_id)),
        "bids" :bids_on_auction,
        "comments":comments_on_auction,
        "value":value,
        "message1":message1
        })
    

def add_comment(request, auction_id):
    global bids_on_auction
    global comments_on_auction

    if request.method == "POST" : 
        print("start")   
        text = request.POST['inputtext']
        print(text)
        item = auction.objects.get(pk=int(auction_id))
        print(item)
        comment0 = comment(created_by = request.user, on_auction =item, comment_text = text )
        print(comment0)
        comment0.save()
        show_items(request, auction_id)
        return render(request, "auctions/item.html",{
          "item":auction.objects.get(pk=int(auction_id)),
          "bids" :bids_on_auction,
          "comments":comments_on_auction
        })
    return render(request, "auctions/index.html",{
          "auctions":auction.objects.all() 
    })       

def add_bid(request, auction_id):
    global bids_on_auction
    global comments_on_auction

    if request.method == "POST" : 
        print("start bid")   
        num = request.POST['inputbid']
        print(num)
        item = auction.objects.get(pk=int(auction_id))
        print(item)
        max_value = item.starting_bid
        current_bids = bid.objects.all()
        print(current_bids)
        for bid0 in current_bids:
            print("^^^^^^^^^^^^")
            print(bid0)
            if bid0.on_auction.title == item.title:
                if (bid0.bid_value) < int(num):
                    bid0.delete()
                    new_bid = bid(created_by = request.user, on_auction =item, bid_value = num )
                    new_bid.save()
                    show_items(request, auction_id)
                    return render(request, "auctions/item.html",{
                        "item":auction.objects.get(pk=int(auction_id)),
                        "bids" :bids_on_auction,
                        "comments":comments_on_auction

                    })
                else:    
                    show_items(request, auction_id)
                    return render(request, "auctions/item.html",{
                        "item":auction.objects.get(pk=int(auction_id)),
                        "bids" :bids_on_auction,
                        "comments":comments_on_auction,
                        "message": "offer is less than Max offer."

                    })
        new_bid = bid(created_by = request.user, on_auction =item, bid_value = num )
        new_bid.save()            
        show_items(request, auction_id)
        return render(request, "auctions/item.html",{
          "item":auction.objects.get(pk=int(auction_id)),
          "bids" :bids_on_auction,
          "comments":comments_on_auction
        })
    return render(request, "auctions/index.html",{
          "auctions":auction.objects.all() 
    })  
def show_items(request, auction_id):
    global bids_on_auction
    global comments_on_auction
    global message1 
    bids = bid.objects.all()
    bids_on_auction = []
    comments_on_auction= []
    item=auction.objects.get(pk=int(auction_id))
    for entry in bids:
        if(entry.on_auction.title == item.title):
            bids_on_auction.append(entry)
            print("firstif")
            if not entry.on_auction.is_active :
                print(request.user)
                if request.user == entry.created_by:
                    message1 = "you win this item"
                    print(entry.created_by)
                    print(message1)
                    flag = True
                else:
                    flag= False
                    message1 = ""    

    comments = comment.objects.all()
    comments_on_auction = []
    for entry in comments:
        if(entry.on_auction.title == item.title):
            comments_on_auction.append(entry)
    print(message1)
    return render(request, "auctions/item.html",{
          "item":auction.objects.get(pk=int(auction_id)),
          "bids" :bids_on_auction,
          "comments":comments_on_auction
        })

def show_categories(request):
    categories = category.objects.all()
    return  render(request, "auctions/category.html",{
      "categories":category.objects.all()  
    })

def show_category(request,id) :
    auction_list= []
    print(id) 
    category0 = category.objects.get(pk=int(id))
    auctions = auction.objects.all()
    for actn in auctions:
        if actn.category == category0:
            auction_list.append(actn)
    print(category0)
    return  render(request, "auctions/index.html", {
        "auctions":auction_list
    }) 

def add_watchlist(request, auction_id):
    flag = True
    print("start add watchlist")
    if request.method == "POST":
        print("*******************")
        auction0 = auction.objects.get(pk = int(auction_id))
        print("*******************")
        watcher0 =request.user
        print("*******************")
        print(watcher0)
        activelisting0 = activelisting.objects.get(watcher=watcher0)
        print("*******************")
        print(activelisting0.active.all())
        print("*******************")
        actives = activelisting0.active.all()
        if auction0 in actives:
            activelisting0.active.remove(auction0)
            status = "btn-success"
            value = "ADD-Item"
        else:    
            activelisting0.active.add(auction0)
            status = "btn-warning"
            value = "Remove-Item"
        print("*******after ************")
        print(activelisting0.active.all())
        print("*******************")
        flag = False
        show_items(request, auction_id)
        return render(request, "auctions/item.html",{
          "item":auction.objects.get(pk=int(auction_id)),
          "bids" :bids_on_auction,
          "comments":comments_on_auction,
          "value":value
        })
      
    return render(request, "auctions/item.html",{
        "item":auction.objects.get(pk=int(auction_id)),
        "bids" :bids_on_auction,
        "comments":comments_on_auction
        })
def Show_watchlist(request): 
        watcher0 =request.user
        print("*******************")
        print(watcher0)
        activelisting0 = activelisting.objects.get(watcher=watcher0)
        actives = activelisting0.active.all() 
        print(actives)
        return render(request, "auctions/watch_list.html",{ 
            "actives": activelisting0.active.all() 
        })  

def active_deactive_Item(request, auction_id):
    if request.method == "POST" :
        auction0 = auction.objects.get(pk = int(auction_id))
        bids = bid.objects.all()
        if auction0.created_by == request.user:
            auction0.is_active= False
            auction0.save()
        for bid0 in bids:
            if bid0.on_auction.title == auction0.title:
                user0 = bid0.created_by
        show_items(request, auction_id)
        print(auction0)
        print(user0)
        return render(request, "auctions/item.html",{
          "item":auction.objects.get(pk=int(auction_id)),
          "bids" :bids,
          "comments":comments_on_auction
        })

    print(auction0)
    print(user0)
    return render(request, "auctions/index.html",{
          "auctions":auction.objects.all()         
    })