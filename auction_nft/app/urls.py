"""auction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.home_page_view, name="home"),
    path("make_an_offer/<str:pk>", views.make_offer_view, name="make_an_offer"),
    path("home_auction/", views.home_auction_view, name="home_auction"),
    path("create_section/", views.create_artwork, name="create_section"),
    path("convert_dollar/", views.conversion_dollar_view, name="convert_dollar"),
    path("show_section/<str:pk>", views.show_artwork, name="show_section"),
    path("buy_now/", views.buy_now, name="buy_now"),
]
