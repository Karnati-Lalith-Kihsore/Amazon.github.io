from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("sell_online", views.sell_online, name="sell_online"),
    path("view_listing/<int:id>", views.view_listing, name="view_listing"),
    path("buy_listing/<int:id>", views.buy_listing, name="buy_listing"),
    path("get_user_details", views.get_user_details, name="get_user_details"),
    path("add_cart/<int:id>", views.add_cart, name="add_cart"),
    path("notification", views.notification, name="notification")
]
