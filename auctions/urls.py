from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path('<int:id>', views.lot, name="lot"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('<int:id>/bid', views.bid, name="bid"),
    path("<int:id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:id>/close", views.close, name="close"),
    path("<int:id>/comment", views.comment, name="comment"),
]
