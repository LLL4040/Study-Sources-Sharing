from django.conf.urls import *
#from django.contrib import admin
from . import view

urlpatterns = [
    url(r'^$', view.page1),
    url(r'^page-download$', view.download),
    url(r'^page-upload$', view.upload),
]
