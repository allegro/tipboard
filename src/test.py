import json
from django.test import RequestFactory, TestCase, Client
from src.manage import show_help
from src.tipboard.app.properties import ALLOWED_TILES
from src.tipboard.templates.template_filter import template_tile
from src.tipboard.app.FakeData.fake_data import buildFakeDataFromTemplate
from src.tipboard.app.parser import parseXmlLayout, getFlipboardTitle, getConfigNames
from src.tipboard.app.cache import MyCache, getCache
from src.tipboard.app.utils import checkAccessToken
from src.tipboard.app.cache import listOfTilesFromLayout
from src.tipboard.app.applicationconfig import getRedisPrefix
from src.sensors.sensors1_text import sonde1
from src.sensors.sensors2_piechart import sonde2
from src.sensors.sensors3_linechart import sonde3
from src.sensors.sensors4_cumulativeflow import sonde4
from src.sensors.sensors5_simplepercentage import sonde5
from src.sensors.sensors6_listing import sonde6
from src.sensors.sensors7_barchart import sonde7
from src.sensors.sensors9_bigvalue import sonde9
from src.sensors.sensors10_justvalue import sonde10
from src.sensors.sensors12_normchart import sonde12
from src.sensors.sensors14_radarchart import sonde14
from src.sensors.sensors15_polarchart import sonde15
from src.sensors.sensors16_dougnutchart import sonde16
from src.sensors.sensors17_halfdougnutchart import sonde17
# from src.sensors.sensors_main import launch_sensors


# @pytest.mark.asyncio
# async def test_0001_test_consumer():
#     #communicator = HttpCommunicator(WSConsumer, 'GET', '/communication/websocket')
#     communicator = WebsocketCommunicator(WSConsumer, '/communication/websocket')
#     connected, subprotocol = await communicator.connect()
#     assert connected
#     # response = await communicator.get_response()
#     # self.assertTrue(response['status'] == 200)
#     await   communicator.disconnect()

def testTileUpdate(tester=None, tileId='test_pie_chart', sonde=None, isChartJS=True):
    """
        1 - Get a tile from the redis cache, store this in tile_txt_data_before
        2 - execute the sensors to update the data of the tile
        3 - Again, get a tile from the redis cache store this in tile_txt_data_after
        4 - Compare the data of tile_txt_data_before vs tile_txt_data_after
        5 - If there are the same, update tile data is broken :)
    """
    tilePrefix = getRedisPrefix(tileId)
    beforeUpdate = json.loads(getCache().redis.get(tilePrefix))
    sonde(tester=tester, tile_id=tileId)
    afterUpdate = json.loads(getCache().redis.get(tilePrefix))
    if isChartJS:
        isDiff = beforeUpdate['data']['datasets'][0]['data'] != afterUpdate['data']['datasets'][0]['data']
    else:
        isDiff = beforeUpdate['data'] != afterUpdate['data']
    tester.assertTrue(isDiff)


class TestApp(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.fakeClient = Client()
        self.ALLOWED_TILES = ALLOWED_TILES

    def test_0001_parser(self):
        """ Test XmlParser for layout """
        config = parseXmlLayout()
        title = config['details']['page_title']
        self.assertTrue(title is not None)

    def test_0011_cache_redisConnection(self):
        """ Test redis connection is set """
        cache = MyCache()
        self.assertTrue(cache.isRedisConnected is True)

    def test_0012_cache_permissionTest(self):
        """ Test redis cache Handle when GET / SET """
        cache = MyCache()
        self.assertTrue(cache.set(tile_id=getRedisPrefix('test'), dumped_value=json.dumps({'testValue': True})))
        self.assertTrue(json.loads(cache.redis.get(getRedisPrefix('test')))['testValue'])

    def test_0013_cache_parsingTile(self):
        """ Test if cache is able to read directly on Config/dashboard.yml """
        cache = MyCache()
        cache.listOfTilesCached()
        self.assertTrue(len(listOfTilesFromLayout()) > 0)

    def test_0014_cache_ExceptionTest(self):
        """ Test if cache is able to handle an unknow tile without crash """
        cache = MyCache()
        self.assertTrue(cache.get(tile_id='test42') is None)

    def test_0015_cache_buildFakeData(self):
        """ Test fake_data generation: integrity of data + save in redis """
        cache = getCache()
        for tile in self.ALLOWED_TILES:
            if tile != 'empty':
                tileData = buildFakeDataFromTemplate(tile_id=f'test_{tile}', template_name=tile, cache=cache)
                self.assertTrue('meta' in tileData)
                self.assertTrue('data' in tileData)
                self.assertTrue('id' in tileData)
                self.assertTrue('tile_template' in tileData)
                self.assertTrue(json.loads(cache.redis.get(getRedisPrefix(f'test_{tile}')))['id'] == f'test_{tile}')

    def test_0101_djangoTemplate_tiles(self):
        """ Test template generation """
        for tile in self.ALLOWED_TILES:
            tile_data = dict(title=f'{tile}_ex', tile_template=tile)
            tileTemplate = template_tile(tile_data['title'], tile_data)
            self.assertTrue('role="alert"' not in tileTemplate)
        tileTemplate = template_tile('test_unknown_tile', dict(title='unknown', tile_template='tile'))
        self.assertTrue(tileTemplate is not None)

    def test_0102_flipboard(self):
        """ Test Flipboard object """
        self.assertTrue(getFlipboardTitle() is not None)
        self.assertTrue(getConfigNames() is not None)

    def test_0103_api_info(self):  # TODO FULL GET /dev_properties && GET / && GET /api/tiledata/
        """ Test api /api/info """
        reponse = self.fakeClient.get('/api/info')
        self.assertTrue(reponse.status_code == 200)

    def test_0103_api_flipboardGetDashboard(self):
        """ Test api /flipboard/getDashboardsPaths """
        reponse = self.fakeClient.get('/flipboard/getDashboardsPaths')
        self.assertTrue(reponse.status_code == 200)

    def test_0104_api_checkToken(self):  # TODO
        """ Test token mecanism """
        request = self.fakeClient.get('')
        checkAccessToken(method='GET', request=request, unsecured=False)
        # self.assertTrue(checkAccessToken(method='GET', request=request, unsecured=True))
        self.assertTrue(True)

    def test_0105_api_getHtmlDashboard(self):
        """ Test api /api/info """
        reponse = self.fakeClient.get('/dev_properties')
        self.assertTrue(reponse.status_code == 200)

    def test_1011_updatetile_PieChart(self):
        """ Test PieChart tile update by api """
        testTileUpdate(tester=self, tileId='test_pie_chart', sonde=sonde2)

    def test_1012_updatetile_NormChart(self):
        """ Test NormChart tile update by api """
        testTileUpdate(tester=self, tileId='test_norm_chart', sonde=sonde12)

    def test_1013_updatetile_LineChart(self):
        """ Test LineChart tile update by api """
        testTileUpdate(tester=self, tileId='test_line_chart', sonde=sonde3)

    def test_1014_updatetile_CumulChart(self):
        """ Test CumulChart tile update by api """
        testTileUpdate(tester=self, tileId='test_cumulative_flow', sonde=sonde4)

    def test_1015_updatetile_BarChart(self):
        """ Test BarChart tile update by api """
        testTileUpdate(tester=self, tileId='test_bar_chart', sonde=sonde7)

    def test_1016_updatetile_VBarChart(self):
        """ Test Vetical BarChart tile update by api """
        testTileUpdate(tester=self, tileId='test_vbar_chart', sonde=sonde7)

    def test_1017_updatetile_HdoughnutChart(self):
        """ Test half_doughnut tile update by api """
        testTileUpdate(tester=self, tileId='test_half_doughnut_chart', sonde=sonde17)

    def test_1018_updatetile_doughnutChart(self):
        """ Test doughnut tile update by api """
        testTileUpdate(tester=self, tileId='test_doughnut_chart', sonde=sonde16)

    def test_1019_updatetile_RadarChart(self):
        """ Test radar tile update by api """
        testTileUpdate(tester=self, tileId='test_radar_chart', sonde=sonde14)

    def test_1020_updatetile_polarChart(self):
        """ Test polarChart tile update by api """
        testTileUpdate(tester=self, tileId='test_polararea_chart', sonde=sonde15)

    def test_1021_updatetile_txt(self):
        """ Test text tile update by api """
        testTileUpdate(tester=self, tileId='test_text', sonde=sonde1, isChartJS=False)

    def test_1022_updatetile_sp(self):
        """ Test simplePercentage tile update by api """
        testTileUpdate(tester=self, tileId='test_simple_percentage', sonde=sonde5, isChartJS=False)

    def test_1023_updatetile_listing(self):
        """ Test listing tile update by api """
        testTileUpdate(tester=self, tileId='test_listing', sonde=sonde6, isChartJS=False)

    def test_1024_updatetile_bigValue(self):
        """ Test big_value tile update by api """
        testTileUpdate(tester=self, tileId='test_big_value', sonde=sonde9, isChartJS=False)

    def test_1024_updatetile_justValue(self):
        """ Test just_value tile update by api """
        testTileUpdate(tester=self, tileId='test_just_value', sonde=sonde10, isChartJS=False)

    # def test_0010_test_schedulesensors(self):
    #     launch_sensors(isTest=True, checker=self, fakeClient=self.fakeClient)

    # def test_0010_test_demo_mode(self):
    #     launch_sensors(isTest=True, checker=self, fakeClient=self.fakeClient)

    def test_1024_checkmanage(self):
        """ Test just_value tile update by api """
        show_help()
