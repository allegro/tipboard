from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url
from django.urls import path
from src.tipboard.app.views.api import push_api, project_info, tile_rest
from src.tipboard.app.views.dashboard import renderHtmlForTiles, getDashboardsPaths
from src.tipboard.app.views.dashboard import renderFlipboardHtml, demo_controller
from swagger_render.views import SwaggerUIView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    # Render View for client
    url(r'^flipboard/getDashboardsPaths$', getDashboardsPaths),

    url(r'^api/tiledata/([a-zA-Z0-9_-]+)$', tile_rest),
    url(r'^api/push$', push_api),
    url(r'^api/info$', project_info),

    url(r'^demo/([a-zA-Z0-9_-]+)$', demo_controller),
    path('swagger/', SwaggerUIView.as_view()),

    url(r'^$', renderFlipboardHtml),
    url(r'^([a-zA-Z0-9_-]*)$', renderHtmlForTiles),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static('/docs/', document_root='docs')
