import time
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler
from src.sensors.sensors1_text import sonde1
from src.sensors.sensors2_piechart import sonde2
from src.sensors.sensors3_linechart import sonde3
from src.sensors.sensors4_cumulativeflow import sonde4
from src.sensors.sensors5_simplepercentage import sonde5
from src.sensors.sensors6_listing import sonde6
from src.sensors.sensors7_barchart import sonde7
# from src.sensors.sensors8_fancylisting import sonde8
from src.sensors.sensors9_bigvalue import sonde9
from src.sensors.sensors10_justvalue import sonde10
from src.sensors.sensors12_normchart import sonde12
# from src.sensors.sensors13_regression import sonde13
from src.sensors.sensors14_radarchart import sonde14
from src.sensors.sensors15_polarchart import sonde15
from src.sensors.sensors16_dougnutchart import sonde16
from src.sensors.sensors17_halfdougnutchart import sonde17
from src.sensors.utils import end


def launch_sensors(isTest=False, checker=None, fakeClient=None):
    # sonde1(isTest)
    # sonde2(isTest, checker, fakeClient)
    # sonde3(isTest)
    # sonde4(isTest)
    # sonde5(isTest)
    # sonde7(isTest, isHorizontal=True)
    # sonde7(isTest, isHorizontal=False)
    # sonde9(isTest)
    # sonde10(isTest)
    # sonde12(isTest)
    # sonde14(isTest)
    # sonde15(isTest)
    # sonde16(isTest)
    scheduleYourSensors(BlockingScheduler())  # If you need actualized data :)


def addSchedule(scheduler, sonde, timeToRun=datetime.now(), second=8):
    second = 1
    scheduler.add_job(sonde, 'interval', seconds=second, next_run_time=timeToRun)


def scheduleYourSensors(scheduler):  # pragma: no cover
    now = datetime.now()
    # scheduler.add_job(sonde1, 'interval', seconds=2)
    # addSchedule(scheduler, sonde2, timeToRun=now + timedelta(milliseconds=100), second=40)
    # addSchedule(scheduler, sonde3, timeToRun=now + timedelta(milliseconds=200), second=3)
    # addSchedule(scheduler, sonde4, timeToRun=now + timedelta(milliseconds=300), second=19)
    # addSchedule(scheduler, sonde5, timeToRun=now + timedelta(milliseconds=400), second=16)
    # scheduler.add_job(sonde6, 'interval', seconds=45)
    # scheduler.add_job(sonde7, 'interval', seconds=1,
    #                   next_run_time=now + timedelta(milliseconds=500), args=[False, False])
    # scheduler.add_job(sonde7, 'interval', seconds=1,
    #                   next_run_time=now + timedelta(milliseconds=600), args=[False, True])
    # addSchedule(scheduler, sonde9, timeToRun=now + timedelta(milliseconds=700), second=39)
    # addSchedule(scheduler, sonde10, timeToRun=now + timedelta(milliseconds=800), second=50)
    # addSchedule(scheduler, sonde12, timeToRun=now + timedelta(milliseconds=900), second=45)
    # addSchedule(scheduler, sonde14, timeToRun=now + timedelta(milliseconds=150), second=2)
    # addSchedule(scheduler, sonde15, timeToRun=now + timedelta(milliseconds=250), second=28)
    addSchedule(scheduler, sonde16, timeToRun=now + timedelta(milliseconds=350), second=30)
    addSchedule(scheduler, sonde17, timeToRun=now + timedelta(milliseconds=350), second=30)
    print(f"(+) Tipboard starting schedul task", flush=True)
    scheduler.start()
    return True


def stopTheSensors(localScheduler):
    if localScheduler is not None:
        localScheduler.shutdown()


if __name__ == "__main__":  # pragma: no cover
    print(f"(+) Tipboard  sensors initialisation", flush=True)
    start_time = time.time()
    # launch_sensors()
    scheduleYourSensors(BlockingScheduler())  # If you need actualized data :)
    end(title="startUp", start_time=start_time)
