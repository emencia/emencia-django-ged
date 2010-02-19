"""Views for emencia.django.ged"""
import os
import mimetypes

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from emencia.django.ged.models import Path
from emencia.django.ged.models import Document

def view_browsing(request, path):
    if path == '/':
        return view_root_browsing(request)
    
    tail, document = os.path.split(path)    
    if document:
        return view_document_detail(request, document)
    return view_path_detail(request, tail)

def view_document_detail(request, document):
    document = get_object_or_404(Document, slug=document)
    type, encoding = mimetypes.guess_type(document.document.url)
    if not type:
        type = 'text/plain'
    response = HttpResponse(mimetype=type)
    response['Content-Disposition'] = 'attachment; filename=%s' % document.document.url

    return response

def view_root_browsing(request):
    directories = Path.objects.filter(parent=None)
    documents = Document.objects.filter(status=1, path=None)
        
    return render_to_response('ged/browse.html',
                              {'path': '/',
                               'directories': directories,
                               'documents': documents},
                              context_instance=RequestContext(request))

def view_path_detail(request, path):
    path_bits = [p for p in path.split('/') if p]
    
    path_obj = None
    for p in get_list_or_404(Path, slug=path_bits[-1]):
        if p.virtual_path() == path:
            path_obj = p
    if not path_obj:
        raise Http404

    directories = path_obj.path_set.all()
    documents = path_obj.document_set.filter(status=1)

    if path_obj.parent:
        parent_url = path_obj.parent.get_absolute_url()
    else:
        parent_url = reverse('ged_root_browsing')
        
    return render_to_response('ged/browse.html',
                              {'path': '/%s/' % path,
                               'parent_url': parent_url,
                               'directories': directories,
                               'documents': documents},
                              context_instance=RequestContext(request))
