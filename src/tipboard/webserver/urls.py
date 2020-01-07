from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url
from src.tipboard.app.views.api import push, projectInfo, tile, meta, update
from src.tipboard.app.views.api_unsecured import push_unsecured, tile_unsecured, meta_unsecured, update_unsecured
from src.tipboard.app.views.dashboard import renderHtmlForTiles, getDashboardsPaths, renderFlipboardHtml
from src.tipboard.app.properties import API_KEY, API_VERSION

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    # Render View for client
    url(r'^flipboard/getDashboardsPaths$', getDashboardsPaths),
    url(r'^$', renderFlipboardHtml),
    url(r'^([a-zA-Z0-9_-]*)$', renderHtmlForTiles),

    # API interaction
    url(r'^api/tiledata/([a-zA-Z0-9_-]+)$', tile),
    url(r'^api/tileconfig/([a-zA-Z0-9_-]+)$', meta),
    url(r'^api/push$', push),
    url(r'^api/update$', update),
    url(r'^api/info$', projectInfo),

    # Unsecured API interaction
    # To not depreciate previous script(of people using tipboard1.0), dont destroy this security issue :D
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/tileconfig/([a-zA-Z0-9_-]+)$', tile_unsecured),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/tileconfig/([a-zA-Z0-9_-]+)$', meta_unsecured),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/push$', push_unsecured),
    url(r'^api/' + API_VERSION + '/' + API_KEY + '/update$', update_unsecured),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
