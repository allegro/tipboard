#!/usr/bin/env python
import os, sys


def startDjango(settings_path='tipboard.webserver.settings'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_path)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    return execute_from_command_line(sys.argv)


def show_help():  # pragma: no cover
    print("""
    Usage:
      -h, or help  \t\t=> show help usage
      -r, or runserver\t=> start the tipboard server
      -s, or sensors \t=> start sensors located in src/sensors """)
    return 0


def main(argc, argv):  # don't you miss the old fashion way, the fabulous main in C :D.    I do
    sys.path.insert(0, os.getcwd())  # Import project to PYTHONPATH
    if "sensors" in argv[1] or '-s' in argv[1]:
        from src.sensors.sensors_main import launch_sensors
        return launch_sensors()
    elif "runserver" in argv[1] or "test" in argv[1]:
        return startDjango()
    else:
        return show_help()


def main_as_pkg():  # pragma: no cover
    """ to become a python package and go to pypi, started in ../setup.py """
    return startDjango(settings_path='src.tipboard.webserver.settings')


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
