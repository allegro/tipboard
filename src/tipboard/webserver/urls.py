from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url
from src.tipboard.app.properties import *
from src.tipboard.app.views.api import push, projectInfo,  tile, meta, update#, deleteTile, getTile
from src.tipboard.app.views.dashboard import dashboardRendererHandler, getDashboardsPaths, flipboardHandler


favicon_view = RedirectView.as_view(url="/static/" + 'favicon.ico', permanent=True)

urlpatterns = [
    url(r'^flipboard/getDashboardsPaths$', getDashboardsPaths),
    url(r'^$', flipboardHandler),
    url(r'^([a-zA-Z0-9_-]*)$', dashboardRendererHandler),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/tiledata/([a-zA-Z0-9_-]+)$', tile),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/tileconfig/([a-zA-Z0-9_-]+)$', meta),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/info$', projectInfo),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/push$', push),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/update$', update),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

