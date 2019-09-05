from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url
from src.tipboard.app.properties import *
from src.tipboard.app.views.api import push, projectInfo,  tile, meta, update
from src.tipboard.app.views.api import push_unsecured, tile_unsecured, meta_unsecured, update_unsecured
from src.tipboard.app.views.dashboard import dashboardRendererHandler, getDashboardsPaths, flipboardHandler

favicon_view = RedirectView.as_view(url="/static/" + 'favicon.ico', permanent=True)

url_tiledata = r'^api/tiledata/([a-zA-Z0-9_-]+)$'
url_meta = r'^api/tileconfig/([a-zA-Z0-9_-]+)$'
url_info = r'^api/info$'
url_push = r'^api/push$'
url_update = r'^api/update$'

# To not depreciate previous script(of people using tipboard1.0), dont destroy this security issue :D
url_tiledata_unsecured = r'^api/' + API_VERSION + '/' + API_KEY + '/tileconfig/([a-zA-Z0-9_-]+)$'
url_meta_unsecured = r'^api/' + API_VERSION + '/' + API_KEY + '/tileconfig/([a-zA-Z0-9_-]+)$'
url_push_unsecured = r'^api/' + API_VERSION + '/' + API_KEY + '/push$'
url_update_unsecured = r'^api/' + API_VERSION + '/' + API_KEY + '/update$'
print('^api/' + API_VERSION + '/' + API_KEY + '/update$')
urlpatterns = [
    # Render View for client
    url(r'^flipboard/getDashboardsPaths$', getDashboardsPaths),
    url(r'^$', flipboardHandler),
    url(r'^([a-zA-Z0-9_-]*)$', dashboardRendererHandler),

    # API interaction
    url(url_tiledata, tile),
    url(url_meta, meta),
    url(url_push, push),
    url(url_info, projectInfo),
    url(url_update, update),

    # Unsecured API interaction
    url(url_tiledata_unsecured, tile_unsecured),
    url(url_meta_unsecured, meta_unsecured),
    url(url_push_unsecured, push_unsecured),
    url(url_update_unsecured, update_unsecured),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

