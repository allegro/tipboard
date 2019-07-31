from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf.urls import url
from tipboard.properties import *


favicon_view = RedirectView.as_view(url="/static/" + 'favicon.ico', permanent=True)

urlpatterns = [

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

