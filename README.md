Tipboard
========

![docs](https://readthedocs.org/projects/tipboard/badge/?version=latest) ![redhat python37:rhel7](https://img.shields.io/badge/redhat-python37:rhel7-brightgreen.svg) ![bitnami python:3.7](https://img.shields.io/badge/bitnami-python:3.7-brightgreen.svg) ![django 2.0](https://img.shields.io/badge/django-2.0-brightgreen.svg)

|    /     | C.I      |  C.D     |  Release |
| -------- | -------- | -------- | -------- |
| Gitlab   | [![Gitlab Build status](https://gitlab.com/the-maux/tipboard/badges/develop/pipeline.svg)](https://gitlab.com/the-maux/tipboard/commits/develop)     | ![pipeline success](https://img.shields.io/badge/pipeline-success-brightgreen.svg)     | ![docker_hub gitlab:1.0.0](https://img.shields.io/badge/docker_hub-gitlab:1.0.0-blue.svg)    |
| Azure    | [![Travis Build Status](https://travis-ci.com/the-maux/tipboard.svg?branch=develop)](https://travis-ci.com/the-maux/tipboard)     | ![pipeline success](https://img.shields.io/badge/pipeline-success-brightgreen.svg)    | ![docker_hub azure:1.0.0](https://img.shields.io/badge/docker_hub-azure:1.0.0-blue.svg)    |
| AWS      | [![CircleCI](https://circleci.com/gh/the-maux/tipboard/tree/master.svg?style=svg)](https://circleci.com/gh/the-maux/tipboard/tree/master)    | [![Gitlab Build status](https://gitlab.com/the-maux/tipboard/badges/develop/pipeline.svg)](https://gitlab.com/the-maux/tipboard/commits/develop)     | ![docker_hub aws:1.0.0](https://img.shields.io/badge/docker_hub-aws:1.0.0-blue.svg) |
| Openshift     | [![Travis Build Status](https://travis-ci.com/the-maux/tipboard.svg?branch=develop)](https://travis-ci.com/the-maux/tipboard)     | ![deploy success](https://img.shields.io/badge/deploy-success-brightgreen.svg)     |![helm tipboard:1.0.0](https://img.shields.io/badge/helm-tipboard:1.0.0-blue.svg)     |
| Travis     | [![Travis Build Status](https://travis-ci.com/the-maux/tipboard.svg?branch=develop)](https://travis-ci.com/the-maux/tipboard)    |     |       |
| Docker     | ![Docker build](https://img.shields.io/docker/cloud/build/themaux/tipboard.svg)     |  | ![docker stars](https://img.shields.io/docker/stars/themaux/tipboard)     |
| Pypi  3   | [![Travis Build Status](https://travis-ci.com/the-maux/tipboard.svg?branch=develop)](https://travis-ci.com/the-maux/tipboard)  |  [![Travis Build Status](https://travis-ci.com/the-maux/tipboard.svg?branch=develop)](https://travis-ci.com/the-maux/tipboard)     | [![PyPI version](https://badge.fury.io/py/tipboard2.svg)](https://badge.fury.io/py/tipboard2) ![Python >=3.7](https://img.shields.io/badge/Python->=3.7-brightgreen.svg)|
| Pypi 2    | [![Gitlab Build status](https://gitlab.com/the-maux/tipboard/badges/develop/pipeline.svg)](https://gitlab.com/the-maux/tipboard/commits/develop)     |  [![Gitlab Build status](https://gitlab.com/the-maux/tipboard/badges/develop/pipeline.svg)](https://gitlab.com/the-maux/tipboard/commits/develop)     | [![PyPI version](https://badge.fury.io/py/tipboard.svg)](https://badge.fury.io/py/tipboard) ![Python 2.7](https://img.shields.io/badge/Python-2.7-red.svg)
|


Introduction
------------

Tipboard is a system for creating dashboards, written in JavaScript and Python.
Its widgets ('tiles' in Tipboard's terminology) are completely
separated from data sources, which provides great flexibility and
relatively high degree of possible customizations.

Because of its intended target (displaying various data and statistics
in your office), it is optimized for larger screens.

A detailed, technical documentation for Tipboard can be found
[here](http://tipboard.readthedocs.org/en/latest/).

Quick start
-----------

### Execution by python

Some required packages need to be present, and python3.7 is required now  
`  $ sudo apt-get install python-dev python-virtualenv redis-server`

<details>
    <summary><b>Install with python dependencies on virtual env</b></summary>
  
```shell
$ virtualenv tb-env                       # create virtual env
$ source tb-env/bin/activate              # activate virtual env
$ (tb-env)$ install -r requirements.txt   # install python lib
$ (tb-env)$ tipboard create_project my_test_dashboard
$ (tb-env)$ python manage.py runserver    # start webserver
```
</details>


<details>
    <summary><b>Install with python dependencies on system</b></summary>
  
```shell
$ pip install -r requirements.txt
$ python manage.py runserver
```
</details>

### Execution by docker

It's a non-root bitnami/python3.7 image

<details>
    <summary><b>By git source</b></summary>
  
```shell
$ docker build -t tipboard:local .
$ docker run -p 8080:8080 tipboard:local
```
</details>
<details>
    <summary><b>By docker hub</b></summary>
  
```shell
$ docker pull themaux/tipboard
$ docker run -p 8080:8080 themaux/tipboard
```
</details>

<details>
    <summary><b>Remove redis from contener</b></summary>
  
     1 - In Dockerfile, comment line 3 `RUN apt-get update && apt-get install redis-server -y`
     2 - In entrypoint.sh, comment line 2 `nohup redis-server &`
     3 - Change the value *REDIS_HOST* & *REDIS_PASSWORD* in the tipboard/Config/properties.json
</details>



### Execution on cloud

<details>
    <summary><b>Deploy on AWS</b></summary>
  
```shell
# From sources git source
$ eb init -p docker tipboard-aws
$ eb create --single
$ eb status
$ eb open
```
</details>

<details>
    <summary><b>Deploy on Openshift</b></summary>
  
```shell
# From docker hub
$ oc new-app themaux/tipboard
# Update the config_layout.yaml
$ oc apply -f ./helm/tipboard-charts-deploy/manifests/tipboard-ops/charts/config/templates/tipboard-configmap.yaml
```
</details>

<details>
    <summary><b>Deploy on Azure</b></summary>
  
```shell
# From docker hub
$ oc new-app themaux/tipboard
# Update the config_layout.yaml
$ oc apply -f ./helm/tipboard-charts-deploy/manifests/tipboard-ops/charts/config/templates/tipboard-configmap.yaml
```
</details>

<details>
    <summary><b>Deploy on clusters kubernets</b></summary>
  
```shell
# Build helm package
$ helm package ./helm/tipboard-charts-template/python3-tipboard --save=false -d ./helm/charts/tipboard-charts-deploy
# Build deployment helm template
$ mkdir manifests
$ helm template --values tipboard_helm.yaml --name tipboard  --output-dir ./manifests .
# Deploy manifest
$ oc apply -R -f ./manifests || helm install --name tipboard MY_PATH_ENVIRONMENT
```
</details>



License
-------

Tipboard is licensed under the [Apache License, v2.0](http://tipboard.readthedocs.org/en/latest/license.html).

Copyright (c) 2013-2017 [Allegro Group](http://allegrogroup.com).
