from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.views.generic.base import RedirectView
from django.conf.urls import url
from tipboard.properties import *
from tipboard.views.api import push, projectInfo, deleteTile, tile, getTile, meta
from tipboard.views.dashboard import dashboardRendererHandler, getDashboardsPaths, flipboardHandler


favicon_view = RedirectView.as_view(url="/static/" + 'favicon.ico', permanent=True)

urlpatterns = [
    url(r'^flipboard/getDashboardsPaths$', getDashboardsPaths),
    url(r'^$', flipboardHandler),
    url(r'^([a-zA-Z0-9_-]*)$', dashboardRendererHandler),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/tiledata/([a-zA-Z0-9_-]+)$', tile),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/tileconfig/([a-zA-Z0-9_-]+)$', meta),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/info$', projectInfo),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/push$', push),
    url(r'^tile/(\w+)/push/$', push),
    #url(r'^$', dashboard)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)