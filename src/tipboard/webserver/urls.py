from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url
from src.tipboard.app.views.api import push_api, project_info, tile_rest
from src.tipboard.app.views.flipboard import getDashboardsPaths, demo_controller, renderFlipboardHtml
from src.tipboard.app.views.flipboard import renderDashboardHtmlUniqueDashboard, renderDashboardHtmlForFlipboard

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r'^flipboard/getDashboardsPaths$', getDashboardsPaths),  # get all dashboard in Config/

    url(r'^api/tiledata/([a-zA-Z0-9_-]+)$', tile_rest),  # get data of a single tile
    url(r'^api/push$', push_api),  # update data for a single tile
    url(r'^api/info$', project_info),  # get data from the tipboard server

    url(r'^demo/([a-zA-Z0-9_-]+)$', demo_controller),  # start a demo with sensors to actualize data

    url(r'^$', renderFlipboardHtml),  # start the flipboard logic for multiple dashboard in a single flipboard.html
    url(r'^([a-zA-Z0-9_-]*)$', renderDashboardHtmlUniqueDashboard),  # render a single dashboard.html
    url(r'^dashboard/([a-zA-Z0-9_-]*)$', renderDashboardHtmlForFlipboard),  # render the tiles html for ws in client js
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
