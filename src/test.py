from django.test import RequestFactory, TestCase, Client
from src.tipboard.app.properties import ALLOWED_TILES
from src.tipboard.templates.template_filter import template_tile
from src.tipboard.app.fake_data import buildFakeDataFromTemplate
from src.tipboard.app.parser import parse_xml_layout
from src.tipboard.app.flipboard import Flipboard
from src.tipboard.app.cache import MyCache
from src.tipboard.app.utils import checkAccessToken
from src.sensors.sensors_main import launch_sensors

class TestApp(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.fakeClient = Client()
        self.ALLOWED_TILES = ALLOWED_TILES

    def test_0010_template_tiles(self):
        """ Test template generation """

        for tile in self.ALLOWED_TILES:
            tile_data = {'title': f"{tile}_ex", 'tile_template': tile}
            tileTemplate = template_tile(tile_data['title'], tile_data)
            self.assertTrue('role="alert"' not in tileTemplate)
        tileTemplate = template_tile("test_unknown_tile", {'title': 'unknown', 'tile_template': 'tile'})
        self.assertTrue(tileTemplate is not None)

    def test_0020_fake_data(self):
        """ Test fake_data generation """

        for tile in self.ALLOWED_TILES:
            if tile != "text" and tile != "empty":
                tileData = buildFakeDataFromTemplate(f"test_{tile}", template_name=tile, cache=None)
                self.assertTrue("meta" in tileData)
                self.assertTrue("data" in tileData)
                self.assertTrue("id" in tileData)
                self.assertTrue("tile_template" in tileData)

    def test_0030_parser(self):
        """ Test XmlParser for layout """
        config = parse_xml_layout()
        title = config['details']['page_title']
        self.assertTrue(title is not None)

    def test_0040_flipboard(self):
        """ Test Flipboard object """
        flipboard = Flipboard()
        self.assertTrue(flipboard.get_flipboard_title() is not None)
        self.assertTrue(flipboard.get_paths() is not None)

    def test_0050_cache(self):
        cache = MyCache()
        self.assertTrue(cache is not None)
        cache.listOfTilesCached()
        self.assertTrue(len(cache.listOfTilesFromLayout()) > 0)
        cache.get(tile_id='test')
        cache.set(tile_id='test', dumped_value={'testValue': True})
        cache.createTile(tile_id='test', value={'test': True}, tile_template='test')

    def test_0060_checkToken(self):
        request = self.fakeClient.get('')
        checkAccessToken(method='GET', request=request, unsecured=True)
        checkAccessToken(method='GET', request=request, unsecured=False)

    def test_0070_api(self):
        from src.tipboard.app.properties import API_KEY, API_VERSION
        self.fakeClient.post('api/' + API_VERSION + '/' + API_KEY + '/update')
        self.fakeClient.post('api/' + API_VERSION + '/' + API_KEY + '/tileconfig/' + 'TEST_TILE')
        self.fakeClient.post('api/' + API_VERSION + '/' + API_KEY + '/push')
        self.fakeClient.post('api/' + API_VERSION + '/' + API_KEY + '/update')
        self.assertTrue(True)

    def test_0080_test_sensors(self):
        launch_sensors(isTest=True)
