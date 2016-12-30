from django.conf.urls import url

from image_manager.views import create_thumbnail
urlpatterns = [
url(r'^create-thumbnail/$', create_thumbnail),]
