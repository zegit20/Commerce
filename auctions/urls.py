from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create_view"),
    path("visit/<int:auction_id>", views.visit_item, name="visit_item"),
    path("comment/<int:auction_id>", views.add_comment, name="add_comment"),
    path("bid/<int:auction_id>", views.add_bid, name="add_bid"),
    path("vist/<int:auction_id>", views.add_watchlist, name="add_watchlist"),
    path("categories/", views.show_categories, name="show_categories"),
    path("categories/<str:id>", views.show_category, name="show_category"),
    path("watchlist/", views.Show_watchlist, name="Show_watchlist"),
    path("inactive/<int:auction_id>", views.active_deactive_Item, name="active_deactive_Item")
  
]

