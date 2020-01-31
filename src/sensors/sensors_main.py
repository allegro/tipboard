import time
# from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from src.sensors.sensors1_text import sonde1
from src.sensors.sensors2_piechart import sonde2
from src.sensors.sensors3_linechart import sonde3
from src.sensors.sensors4_cumulativeflow import sonde4
from src.sensors.sensors5_simplepercentage import sonde5
# from src.sensors.sensors6_listing import sonde6
from src.sensors.sensors7_barchart import sonde7
from src.sensors.sensors9_bigvalue import sonde9
from src.sensors.sensors10_justvalue import sonde10
from src.sensors.sensors12_normchart import sonde12
from src.sensors.sensors14_radarchart import sonde14
from src.sensors.sensors15_polarchart import sonde15
from src.sensors.sensors16_dougnutchart import sonde16
from src.sensors.sensors17_halfdougnutchart import sonde17
from src.sensors.utils import end


def addSchedule(scheduler, sonde, second=8, args=None):
    if args is None:
        scheduler.add_job(sonde, 'interval', seconds=second)
    else:
        scheduler.add_job(sonde, 'interval', seconds=second, args=args)


def scheduleYourSensors(scheduler=None, tester=None):
    scheduler.add_job(sonde1, 'interval', seconds=2, args=[tester, 'txt_ex'])
    addSchedule(scheduler, sonde2, second=40, args=[tester, 'pie_chartjs_ex'])
    addSchedule(scheduler, sonde3, second=3, args=[tester, 'line_chart_ex'])
    addSchedule(scheduler, sonde4, second=19, args=[tester, 'cfjs_ex'])
    addSchedule(scheduler, sonde5, second=16, args=[tester, 'sp_ex'])
    # scheduler.add_job(sonde6, 'interval', seconds=45)
    scheduler.add_job(sonde7, 'interval', seconds=1, args=[tester, 'barjs_ex', False])
    scheduler.add_job(sonde7, 'interval', seconds=1, args=[tester, 'vbarjs_ex', True])
    addSchedule(scheduler, sonde9, second=39, args=[tester, 'bv_ex'])
    addSchedule(scheduler, sonde10, second=50, args=[tester, 'jv_ex'])
    addSchedule(scheduler, sonde12, second=45, args=[tester, 'norm_chart'])
    addSchedule(scheduler, sonde14, second=2, args=[tester, 'radar_chart'])
    addSchedule(scheduler, sonde15, second=28, args=[tester, 'polararea_ex'])
    addSchedule(scheduler, sonde16, second=30, args=[tester, 'doughnut_ex'])
    addSchedule(scheduler, sonde17, second=30, args=[tester, 'half_doughnut_ex'])
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
