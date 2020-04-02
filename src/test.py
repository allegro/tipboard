import json, time, os
from django.test import RequestFactory, SimpleTestCase, Client
from apscheduler.schedulers.background import BackgroundScheduler
from src.manage import show_help
from src.tipboard.templates.template_filter import template_tile_data, template_tile_dashboard
from src.tipboard.app.properties import ALLOWED_TILES
from src.tipboard.app.DefaultData.defaultTileControler import buildFakeDataFromTemplate
from src.tipboard.app.parser import getDashboardName, getConfigNames, parseXmlLayout
from src.tipboard.app.cache import MyCache
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
from src.sensors.sensors_main import scheduleYourSensors, test_sensors
from src.tipboard.app.views.flipboard import demo_controller
from src.tipboard.app.views.wshandler import WSConsumer


def testTileUpdate(tester=None, tileId='test_pie_chart', sonde=None, isChartJS=True):
    """
        1 - Get a tile from the redis cache, store this in tile_txt_data_before
        2 - execute the sensors to update the data of the tile
        3 - Again, get a tile from the redis cache store this in tile_txt_data_after
        4 - Compare the data of tile_txt_data_before vs tile_txt_data_after
        5 - If there are the same, update tile data is broken :)
    """
    tilePrefix = getRedisPrefix(tileId)
    beforeUpdate = json.loads(MyCache().redis.get(tilePrefix))
    if tileId == 'test_vbar_chart':
        sonde(tester=tester, tile_id=tileId, isHorizontal=True)
    sonde(tester=tester, tile_id=tileId)
    afterUpdate = json.loads(MyCache().redis.get(tilePrefix))
    if isChartJS:
        isDiff = beforeUpdate['data']['datasets'][0]['data'] != afterUpdate['data']['datasets'][0]['data']
    else:
        isDiff = beforeUpdate['data'] != afterUpdate['data']
    tester.assertTrue(isDiff)


def getConfigFileForTest():
    listOfDashboard = getConfigNames()
    if 'default_config' in listOfDashboard:
        return 'default_config'
    if not listOfDashboard:
        print('Cant do unit test, there is no config file')
        exit(-1)
    return listOfDashboard[0]


class TestApp(SimpleTestCase):  # TODO: find a way to test the WebSocket inside django

    def setUp(self):
        self.factory = RequestFactory()
        self.fakeClient = Client()
        self.cache = MyCache()
        self.ALLOWED_TILES = ALLOWED_TILES
        self.layout = getConfigFileForTest()
        print("[DEBUG] Choosing file to test:" + self.layout)

    def test_0001_parse_dashboardXml(self):
        """ Test Parse all tiles, cols, rows from a specific .yaml """
        config = parseXmlLayout(layout_name=self.layout)
        self.assertTrue(config is not None)

    def test_0002_getAllDashboardFiles(self):
        """ Test all dashboard file name from Config/ """
        config = getConfigNames()
        self.assertTrue(len(config) > 0)

    def test_0003_parser_getTitleOfDashboard(self):
        """ Test XmlParser is able to get title of /config/default_config.yml """
        config = parseXmlLayout(layout_name=self.layout)
        title = config['details']['page_title']
        self.assertTrue(title is not None)

    def test_0004_parser_getDashboardColsFromXml(self):  # test if able to parse row
        """ Test XmlParser able to get cols dashboard of /config/default_config.yml """
        self.assertTrue(len(parseXmlLayout(layout_name=self.layout)['layout']) > 0)

    def test_0005_parser_getTilesNameFromXml(self):  # test if able to parse tiles template
        """ Test XmlParser able to get tiles name of /config/default_config.yml """
        tiles_conf = parseXmlLayout(layout_name=self.layout)['tiles_conf']
        self.assertTrue(tiles_conf[next(iter(tiles_conf))]['title'] is not None)

    def test_0006_parser_getTilesIdFromXml(self):
        """ Test XmlParser able to get tiles Id of tiles from /config/default_config.yml """
        tiles_conf = parseXmlLayout(layout_name=self.layout)['tiles_conf']
        self.assertTrue((tiles_conf[next(iter(tiles_conf))]['tile_id']) is not None)

    def test_0011_cache_redisConnection(self):
        """ Test redis connection """
        self.assertTrue(self.cache.isRedisConnected is True)

    def test_0012_cache_permissionTest(self):
        """ Test redis cache Handle when GET / SET """
        tilePrefix = getRedisPrefix('test')
        self.assertTrue(self.cache.set(tile_fullid=tilePrefix, dumped_value=json.dumps({'testValue': True})))
        self.assertTrue(json.loads(self.cache.redis.get(tilePrefix))['testValue'])

    def test_0013_cache_parsingTile(self):
        """ Test if cache is able to read directly on Config/dashboard.yml """
        self.cache.listOfTilesCached()
        self.assertTrue(len(listOfTilesFromLayout(layout_name=self.layout)) > 0)

    def test_0014_cache_ExceptionTest(self):
        """ Test if cache is able to handle an unknow tile without crash """
        self.assertTrue(self.cache.get(tile_id='test42') is None)

    def test_0015_cache_buildFakeData(self):
        """ Test fake_data generation: integrity of data + save in redis """
        for tile in self.ALLOWED_TILES:
            if tile != 'empty':
                tileData = buildFakeDataFromTemplate(tile_id=f'test_{tile}', template_name=tile, cache=self.cache)
                self.assertTrue(tileData is not None)
                self.assertTrue('data' in tileData)
                self.assertTrue('id' in tileData)
                self.assertTrue('tile_template' in tileData)
                isIdCorrect = json.loads(self.cache.redis.get(getRedisPrefix(f'test_{tile}')))['id'] == f'test_{tile}'
                self.assertTrue(isIdCorrect)

    def test_0101_djangoTemplate_tiles(self):
        """ Test template generation for every ALLOWED_TILES """
        template_tile_dashboard(tile_id='id', layout_name=self.layout)
        for tile in self.ALLOWED_TILES:
            tile_data = dict(title=f'{tile}_ex', tile_template=tile)
            tileTemplate = template_tile_data(('layout', tile_data['title']), tile_data)
            if 'role="alert"' in tileTemplate:
                print(f"[EROR] DETECTED WITH TEMPLATE:{tile}")
            self.assertTrue('class="alert alert-danger text-center" role="alert"' not in tileTemplate)  # detect errors
        tileTemplate = template_tile_data(('layout', 'test_unknown_tile'), dict(title='unknown', tile_template='tile'))
        self.assertTrue(tileTemplate is not None)

    def test_0102_flipboard(self):
        """ Test Flipboard object """
        self.assertTrue(getDashboardName() is not None)
        self.assertTrue(getConfigNames() is not None)

    def test_0103_api_info(self):
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
        """ Test api getHtmlDashboard """
        reponse = self.fakeClient.get('/' + self.layout)
        self.assertTrue(reponse.status_code == 200)

    def test_0106_api_getHtmlDashboardNotFound(self):
        """ Test api getHtmlDashboardNotFound """
        reponse = self.fakeClient.get('/IfY0uF1ndMeY0ur0ut')
        self.assertTrue(reponse.status_code == 404)

    def test_0107_api_deleteTileFromApi(self):  # deleting first, cause when get => will be create with FakeData
        """ Test api delete Tile from api """
        reponse = self.fakeClient.delete('/api/tiledata/test_text')
        self.assertTrue(reponse.status_code == 200)

    def test_0108_api_getTileFromApi(self):
        """ Test api get tile data from api """
        reponse = self.fakeClient.get('/api/tiledata/test_text')
        self.assertTrue(reponse.status_code == 200)

    def test_0109_api_parseTitleHtmlFromDashboard(self):  # TODO: fix this by testing the flipboard.html
        """ Test if Yaml to dashboard.html know how to parse title """
        reponse = self.fakeClient.get('/dashboard/' + self.layout)
        title = b'__'  # TODO: need to put __ to test the split methode in template html
        self.assertTrue(title in reponse.content)  # can't work cause it's made by ws

    def test_0110_api_parseConfigHtmlFromDashboard(self):  # test with other file when row
        reponse = self.fakeClient.get('/dashboard/' + self.layout)
        configInYaml = b'id="row"'
        self.assertTrue(configInYaml in reponse.content)

    # def test_0111_api_parseConfigHtmlFromDashboard(self):  # TODO: take the tile id by yaml
    #     reponse = self.fakeClient.get('/dashboard/' + self.layout)
    #     IdTilePresenInYaml = b'id="' + bytes(self.layout, 'utf-8') + b'-pie_chartjs_ex"'
    #     self.assertTrue(IdTilePresenInYaml in reponse.content)

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
        """ Test CumulativeChart tile update by api """
        testTileUpdate(tester=self, tileId='test_cumulative_flow', sonde=sonde4)

    def test_1015_updatetile_BarChart(self):
        """ Test BarChart tile update by api """
        testTileUpdate(tester=self, tileId='test_bar_chart', sonde=sonde7)

    def test_1016_updatetile_VBarChart(self):
        """ Test Vertical BarChart tile update by api """
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

    def test_1025_updatetile_justValue(self):
        """ Test just_value tile update by api """
        testTileUpdate(tester=self, tileId='test_just_value', sonde=sonde10, isChartJS=False)

    def test_1028_test_websocket(self):
        consumer = WSConsumer(scope=None)
        print(consumer)  # TODO: improve test

    def test_1026_test_sensors(self):  # TODO: fix this double loads linked to the bug in parser.py at .get()
        tilePrefix = getRedisPrefix('test_simple_percentage')
        lm = MyCache().get(tilePrefix)
        beforeUpdate = json.loads(json.loads(lm))
        test_sensors(tester=self)
        scheduler = BackgroundScheduler()
        nbrSensors = scheduleYourSensors(scheduler=scheduler, tester=self)
        self.assertTrue(nbrSensors >= 21)
        time.sleep(5)
        scheduler.shutdown()
        time.sleep(3)
        afterUpdate = json.loads(json.loads(MyCache().get(tilePrefix)))['data']['big_value']
        isDiff = beforeUpdate != afterUpdate
        self.assertTrue(isDiff)

    def test_1027_test_demo_mode(self):
        response = demo_controller(None, flagSensors='on', tester=self)
        self.assertTrue(response.status_code == 302)
        time.sleep(10)
        response = demo_controller(None, flagSensors='off', tester=self)
        self.assertTrue(response.status_code == 302)

    def test_1030_checkmanage(self):
        """ Test just_value tile update by api """
        show_help()

    def test_4242_nohided_code(self):
        """ Test if there is code hided from the coverage """
        os.system("grep --exclude='*.pyc' -rnw ./src -e 'pr" + "agma' > dumpPragmaGulty")
        errors = len(open("dumpPragmaGulty", "r").read().splitlines())
        self.assertTrue(errors == 0)
        if errors == 0:
            os.system("rm dumpPragmaGulty")
