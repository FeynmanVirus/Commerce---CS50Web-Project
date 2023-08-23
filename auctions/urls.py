from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create"),
    path("listing/<str:title>", views.show_listing, name="goto"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("category/<str:category>", views.show_category, name="category"),
    path("categories/", views.categories, name="categories")
]
