from django.conf.urls import patterns, url
from django.views.generic.list import ListView

from gallery.models import PhotoSet
from gallery.views import gallery_detail


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=PhotoSet.objects.all()),
        name='gallery_list'),
    url(r'^(?P<slug>[-\w]+)/$', gallery_detail, name='gallery_detail'),
)
