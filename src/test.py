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

    def test_0020_test_fake_data(self):
        """ Test fake_data generation """

        for tile in self.ALLOWED_TILES:
            if tile is not "text" and tile is not "empty":
                tileData = buildFakeDataFromTemplate(f"test_{tile}", template_name=tile, cache=None)
                self.assertTrue("meta" in tileData)
                self.assertTrue("data" in tileData)
                self.assertTrue("id" in tileData)
                self.assertTrue("tile_template" in tileData)
