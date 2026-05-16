from django.contrib import admin
from django.urls import path,  include
import profile_1.views
urlpatterns = [
    path("", profile_1.views.home, name="home"),
    path("portfolio-single/<str:name>/", profile_1.views.portfolio_single, name="portfolio_single"),
]

