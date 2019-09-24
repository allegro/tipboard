from django.test import RequestFactory, TestCase
from src.tipboard.app.properties import ALLOWED_TILES
from src.tipboard.templates.template_filter import template_tile
from src.tipboard.app.fake_data import buildFakeDataFromTemplate
from src.tipboard.app.properties import API_KEY, API_VERSION
from src.tipboard.app.views.dashboard import dashboardRendererHandler


class TestApp(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.ALLOWED_TILES = ALLOWED_TILES

    def test_0010_template_tiles(self):
        """ Test template generation """

        for tile in self.ALLOWED_TILES:
            tile_data = {'title': f"{tile}_ex", 'tile_template': tile}
            tileTemplate = template_tile(tile_data['title'], tile_data)
            self.assertTrue('role="alert"' not in tileTemplate)

    # def test_0020_fake_data(self):
    #     """ Test Fake data generation """
    #
    #     for tile in self.ALLOWED_TILES:
    #         data = buildFakeDataFromTemplate(tile_id=f"{tile}_ex", template_name=tile, cache=None)
    #         self.assertTrue(data is not None)

    # def test_0030_parser(self):
    #     """ Test Fake data generation """
    #     self.assertTrue(True)
    #
    #
    # def test_0040_api(self):
    #     """ Test Fake data generation """
    #     request = self.factory.get('/api/info')
    #     l = dashboardRendererHandler(request)
    #     self.assertTrue(l.status_code is 200)
    #
    # def test_0050_oldapi(self):
    #     """ Test Fake data generation """
    #     request = self.factory.get('/api/' + API_VERSION + '/' + API_KEY + '/info')
    #     l = dashboardRendererHandler(request)
    #     self.assertTrue(l.status_code is 200)
    #
