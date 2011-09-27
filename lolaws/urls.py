from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.views.generic.simple import redirect_to
from django.contrib import admin

admin.autodiscover()

handler404 = 'lolaws.core.views.server_error'
handler500 = 'lolaws.core.views.server_error'

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url':'/uploadr/'}),
    url(r'^uploadr/', include('lolaws.uploadr.urls')),
    #url(r'^lolaws/', include('lolaws.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

_media_url = settings.MEDIA_URL
if _media_url.startswith('/'):
    _media_url = _media_url[1:]
urlpatterns += patterns('',
    # Serve a favicon, to get rid of those irritating 404 log statements
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': '{0}favicon.ico'.format(_media_url), 'permanant': False}),
    (r'^{0}(?P<path>.*)$'.format(_media_url), 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    # TODO - for AWS stuff
    #(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.UPLOAD_ROOT}),
)
