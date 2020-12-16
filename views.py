from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from gallery.models import PhotoSet


def gallery_detail(request, slug):
    gallery = get_object_or_404(PhotoSet, slug=slug)

    return render_to_response('gallery/photoset_detail.html',
        {'object': gallery},
        context_instance=RequestContext(request))
