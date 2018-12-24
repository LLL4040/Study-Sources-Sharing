from django.conf.urls import *
#from django.contrib import admin
from . import view

urlpatterns = [
    url(r'^index$', view.index),
    url(r'^about$', view.about),
    url(r'^sources$', view.download),
    url(r'^search$', view.download),
    url(r'^upload$', view.upload),
    url(r'^contact$', view.contact),
    url(r'^login$', view.login),
    url(r'^page-keep$', view.keep),
]
