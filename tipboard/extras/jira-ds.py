#!/usr/bin/env python

"""
Jira-ds - a command line utility for fetching various data from Jira.

Usage:
  jira-ds.py --project=NAME (--summary|--cvsr|--issues-counts)
  jira-ds.py --board=NAME (--control-chart|--velocity)
  jira-ds.py --jql=QUERY [-m <limit>]
  jira-ds.py -h | --help

Options:
  --project=NAME   Project name (case sensitive).
  --board=NAME     Board name (case sensitive).
  --jql=QUERY      Return raw data using JQL (Jira Query Language) query.
                   Beware that some queries may be quite heavy on resources!
  -m <limit>       Set 'maxResults' for '--jql' option [default: 1000].
                   (hint: setting it to '0' gives you total number of results
                   without fetching the data)
  --summary        Get issues counts from 'summary' tab.
  --cvsr           Get data table from 'created vs resolved' report
                   (past month).
  --issues-counts  Get issues counts grouped by priority, status, type etc.
  --control-chart  Get data table from 'control chart' report (past month).
  --velocity       Get data table from 'velocity chart' report.
  -h --help        Show this screen.

"""

import json
import os
import requests
import subprocess

from docopt import docopt

JIRA_BASE_URL = ''  # needs to be filled in
JIRA_API_URL = JIRA_BASE_URL + '/rest/api/2/'
GREENHOPPER_API_URL = JIRA_BASE_URL + '/rest/greenhopper/1.0/'
JIRA_CREDENTIALS = {  # needs to be filled in
    'user': '',
    'password': '',
}
SUBP_ENV = os.environ.copy()
SUBP_ENV['JIRA_USER'] = JIRA_CREDENTIALS.get('user')
SUBP_ENV['JIRA_PASSWORD'] = JIRA_CREDENTIALS.get('password')
SUBP_PARAMS = ["casperjs", "jira-ds.js"]
REQUESTS_TIMEOUT = 10  # in seconds


##### 'Internal' stuff.

def _get_identifiers(name, url):
    """
    Gets project_id and project_key (when 'url' points to project) or board_id
    (when 'url' points to board).
    """
    session = requests.Session()
    resp = session.get(url, timeout=REQUESTS_TIMEOUT, params={
        'os_authType': 'basic',
        'os_username': JIRA_CREDENTIALS.get('user'),
        'os_password': JIRA_CREDENTIALS.get('password'),
    })
    resp.raise_for_status()
    rest_data = resp.json()
    try:
        data = rest_data.get('views')  # for boards
    except AttributeError:
        data = rest_data  # for projects
    for d in data:
        if d.get('name') == name:
            return (d.get('id'), d.get('key'))
    return (None, None)  # board/project doesn't exist


def _get_data_from_subprocess(subp_params):
    try:
        data = subprocess.check_output(subp_params, env=SUBP_ENV)
    except subprocess.CalledProcessError as e:
        print("Error in jira-ds.js script: '{}'.".format(e.output.strip()))
        return
    else:
        return json.loads(data)


##### Command-line options.

def get_summary(project_key):
    subp_params = SUBP_PARAMS + ["--project-key=" + project_key,
                                 "--step=summary"]
    return _get_data_from_subprocess(subp_params)


def get_cvsr(project_id):
    subp_params = SUBP_PARAMS + ["--project-id=" + project_id, "--step=cvsr"]
    return _get_data_from_subprocess(subp_params)


def get_issues_counts(project_key):
    subp_params = SUBP_PARAMS + ["--project-key=" + project_key,
                                 "--step=issues-counts"]
    return _get_data_from_subprocess(subp_params)


def get_control_chart(board_id):
    subp_params = SUBP_PARAMS + ["--board-id=" + str(board_id),
                                 "--step=control-chart"]
    return _get_data_from_subprocess(subp_params)


def get_velocity(board_id):
    subp_params = SUBP_PARAMS + ["--board-id=" + str(board_id),
                                 "--step=velocity"]
    return _get_data_from_subprocess(subp_params)


def get_jql(query, max_results):
    session = requests.Session()
    query_url = JIRA_API_URL + 'search?'
    resp = session.get(query_url, timeout=REQUESTS_TIMEOUT, params={
        'os_authType': 'basic',
        'os_username': JIRA_CREDENTIALS.get('user'),
        'os_password': JIRA_CREDENTIALS.get('password'),
        'start-index': 0,
        'maxResults': max_results,
        'jql': query,
    })
    resp.raise_for_status()
    rest_data = resp.json()
    return(rest_data)


##### Putting it all together.

def main():
    args = docopt(__doc__)
    project_name = args.get('--project')
    board_name = args.get('--board')
    jql = args.get('--jql')
    if project_name:
        url = JIRA_API_URL + 'project'
        try:
            project_id, project_key = _get_identifiers(project_name, url)
        except requests.exceptions.RequestException as e:
            print("Your query has raised an error: '{}'.".format(e.message))
            return
        else:
            if not project_id:
                print("Project '{}' does not exist.").format(project_name)
                return
            if args.get('--summary'):
                result = get_summary(project_key)
            elif args.get('--cvsr'):
                result = get_cvsr(project_id)
            elif args.get('--issues-counts'):
                result = get_issues_counts(project_key)
    elif board_name:
        url = GREENHOPPER_API_URL + 'rapidview'
        try:
            board_id, _ = _get_identifiers(board_name, url)
        except requests.exceptions.RequestException as e:
            print("Your query has raised an error: '{}'.".format(e.message))
            return
        else:
            if not board_id:
                print("Board '{}' does not exist.").format(board_name)
                return
            if args.get('--control-chart'):
                result = get_control_chart(board_id)
            elif args.get('--velocity'):
                result = get_velocity(board_id)
    elif jql:
        max_results = args.get('-m')
        try:
            result = get_jql(jql, max_results)
        except requests.exceptions.RequestException as e:
            print("Your query has raised an error: '{}'.".format(e.message))
            return
    print(json.dumps(result, ensure_ascii=False))

if __name__ == '__main__':
    main()
