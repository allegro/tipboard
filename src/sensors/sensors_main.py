import time, datetime, random
from apscheduler.schedulers.blocking import BlockingScheduler
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
from src.sensors.sensors18_gauge import sonde18
from src.sensors.sensors19_lineargauge import sonde19
from src.sensors.sensors20_radialgauge import sonde20
from src.sensors.sensors21_stream import sonde21 as sonde_stream
from src.sensors.sensors21_iframe import sonde21 as sonde_iframe
from src.sensors.sensors22_custom import sonde22
from src.sensors.utils import end


def addSchedule(scheduler, sonde, second=8, args=None):
    scheduler.add_job(sonde, 'interval', seconds=30, args=args, next_run_time=datetime.datetime.now())


def test_sensors(tester):
    sonde1(tester, 'txt_ex')
    sonde2(tester, 'pie_chartjs_ex')
    sonde3(tester, 'line_chart_ex')
    sonde4(tester, 'cfjs_ex')
    sonde5(tester, 'sp_ex')
    sonde6(tester, 'listing_ex')
    sonde7(tester, 'barjs_ex')
    sonde7(tester, 'vbarjs_ex')
    sonde9(tester, 'bv_ex')
    sonde10(tester, 'jv_ex')
    sonde12(tester, 'norm_chart')
    sonde14(tester, 'radar_chart')
    sonde15(tester, 'polararea_ex')
    sonde16(tester, 'doughnut_ex')
    sonde17(tester, 'half_doughnut_ex')
    sonde18(tester, 'gauge_ex')
    sonde19(tester, 'lgauge_ex')
    sonde20(tester, 'rgauge_ex')
    sonde_stream(tester, 'stream_ex')
    sonde_iframe(tester, 'iframe_ex')
    sonde22(tester, 'custom_ex  ')


def scheduleYourSensors(scheduler=None, tester=None):
    if not scheduler.running:
        # scheduler.add_job(sonde1, 'interval', seconds=5, args=[tester, 'txt_ex'])
        # addSchedule(scheduler, sonde2, second=40, args=[tester, 'pie_chartjs_ex'])
        # addSchedule(scheduler, sonde3, second=3, args=[tester, 'line_chartjs_ex'])
        # addSchedule(scheduler, sonde4, second=19, args=[tester, 'cfjs_ex'])
        # addSchedule(scheduler, sonde5, second=16, args=[tester, 'sp_ex'])
        # addSchedule(scheduler, sonde6, second=2, args=[tester, 'listing_ex'])
        # addSchedule(scheduler, sonde7, second=2, args=[tester, 'barjs_ex', False])
        # addSchedule(scheduler, sonde7, second=2, args=[tester, 'vbarjs_ex', True])
        # addSchedule(scheduler, sonde9, second=39, args=[tester, 'bv_ex'])
        # addSchedule(scheduler, sonde10, second=50, args=[tester, 'jv_ex'])
        # addSchedule(scheduler, sonde12, second=45, args=[tester, 'normjs_ex'])
        # addSchedule(scheduler, sonde14, second=2, args=[tester, 'radar_ex'])
        # addSchedule(scheduler, sonde15, second=28, args=[tester, 'polararea_ex'])
        # addSchedule(scheduler, sonde16, second=30, args=[tester, 'doughnut_ex'])
        # addSchedule(scheduler, sonde17, second=30, args=[tester, 'half_doughnut_ex'])
        # addSchedule(scheduler, sonde18, second=30, args=[tester, 'gauge_ex'])
        # addSchedule(scheduler, sonde19, second=30, args=[tester, 'lgauge_ex'])
        # addSchedule(scheduler, sonde20, second=30, args=[tester, 'rgauge_ex'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex1'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex2'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex3'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex4'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex5'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex6'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex6'])
        # addSchedule(scheduler, sonde_iframe, second=30, args=[tester, 'stream_ex8'])
        # addSchedule(scheduler, sonde_stream, second=30, args=[tester, 'stream_ex8'])
        # addSchedule(scheduler, sonde22, second=30, args=[tester, 'custom_ex'])
        print(f"(+) Tipboard starting schedul task", flush=True)
        scheduler.start()
    return scheduler


def stopTheSensors(localScheduler):
    if localScheduler is not None:
        localScheduler.shutdown()


if __name__ == "__main__":
    print(f"(+) Tipboard  sensors initialisation", flush=True)
    start_time = time.time()
    scheduleYourSensors(BlockingScheduler())  # If you need actualized data :)
    end(title="startUp", startTime=start_time)
