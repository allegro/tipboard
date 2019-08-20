#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os, sys


def startDjango():
    sys.path.insert(0, os.getcwd())  # Import project to PYTHONPATH
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def show_help():
    help = """Usage:
  -h, or help  \t\t=> show help usage
  -r, or runserver\t=> start the tipboard server
  -s, or sensors \t=> start sensors located in src/sensors
                """
    print(help)
    return 0


def main(argv, argc):#don't you miss the old fashion way, the fabulous main in C :D.    I do
    if argc == 1:
        return startDjango()
    elif argc == 2:
        if "help" in argv[1] or '-h' in argv[1]:
            return show_help()
        elif "sensors" in argv[1] or '-s' in argv[1]:
            return show_help()  # TODO replace by real sensors
    elif argc >= 2 and "runserver" in argv[1] or '-r' in argv[1]:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tipboard.webserver.settings')
        return startDjango()
    return show_help()


# to become a python package and go to pypi, started in ../setup.py
def main_as_pkg():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.tipboard.webserver.settings')
    startDjango()


if __name__ == '__main__':
    main(sys.argv, len(sys.argv))
