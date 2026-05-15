from django.contrib import admin
from django.urls import path,  include
import profile_1.views
urlpatterns = [
    path("", profile_1.views.home, name="home"),
]
