
# Tipboard :bar_chart: :chart_with_upwards_trend:

 [![][14]][13] [![][11]][13] ![](https://img.shields.io/github/downloads/the-maux/tipboard/total)
![bitnami python:3.7](https://img.shields.io/badge/bitnami-python:3.7-brightgreen.svg) ![bitnami redis](https://img.shields.io/badge/bitnami-redis:5.0-brightgreen.svg) ![django](https://img.shields.io/badge/django-2.0-brightgreen.svg)  

---


## Introduction

Tipboard is a system for creating dashboards, written in JavaScript and Python.
Its widgets ('tiles' in Tipboard's terminology) are completely
separated from data sources, which provides great flexibility and
relatively high degree of possible customizations.

Because of its intended target (displaying various data and statistics
in your office), it is optimized for larger screens.

A detailed, technical documentation for Tipboard can be found
[here](http://tipboard.readthedocs.org/en/latest/).


## Quick start

### 1. Execution by python :snake:

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

### 2. Execution by docker :whale:

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



### 3. Execution on cloud :cloud:

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
# Update the config_layout.yaml  & properties.json
$ oc apply -f ./helm/tipboard-charts-deploy/manifests/tipboard-ops/charts/config/templates/tipboard-configmap.yaml
```
</details>

<details>
    <summary><b>Deploy on Azure</b></summary>
  
```shell
```
</details>

<details>
    <summary><b>Deploy on GCP</b></summary>

```shell
# Go to GCP cloud shell
$ git clone https://github.com/the-maux/tipboard.git
$ gcloud app deploy
# Connect throw your instance with SSH (or scp the right files :D)
# Update the config_layout.yaml & properties.json
```
</details>

<details>
    <summary><b>Deploy on clusters kubernets with helm</b></summary>
  
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


---


### C.I :hammer:

|  Registry  |         Runner       |       Release     |
| --------   | -------------------- | ----------------- |
| Docs       | ![docs](https://readthedocs.org/projects/tipboard/badge/?version=latest) | [here](https://readthedocs.org/projects/tipboard/badge/?version=latest)    |
| pypi       |  [![CircleCI][1]][2] | [![][9]][10]  |
| Github     |  [![Gitlab][17]][4]   | [![Gitlab][3]][4]  |
| DockerHUB  |  [![][15]][13]       | [![][16]][13] |
| Helm       |  [![Gitlab][7]][8]   | [![Gitlab][7]][8]   |

[1]: https://travis-ci.com/the-maux/tipboard.svg?branch=develop
[2]: https://travis-ci.com/the-maux/tipboard
[3]: https://img.shields.io/github/v/release/the-maux/tipboard
[4]: https://github.com/the-maux/tipboard/packages
[5]: https://img.shields.io/badge/pipeline-todo-orange
[6]: https://gitlab.com/the-maux/tipboard/commits/develop
[7]: https://img.shields.io/badge/pipeline-todo-orange
[8]: https://gitlab.com/the-maux/tipboard/commits/develop
[9]: https://badge.fury.io/py/tipboard2.svg
[10]: https://pypi.org/project/tipboard2.0/
[11]: https://img.shields.io/docker/stars/themaux/tipboard
[12]: https://pypi.org/project/tipboard2.0/
[13]: https://hub.docker.com/r/themaux/tipboard
[14]: https://img.shields.io/docker/pulls/themaux/tipboard
[15]: https://img.shields.io/docker/cloud/automated/themaux/tipboard
[16]: https://img.shields.io/docker/cloud/build/themaux/tipboard
[17]: https://gitlab.com/the-maux/tipboard/badges/master/pipeline.svg





### C.D :tada:

|   Registry    |         Pipeline       |      HowTo     |
| ------------- | -------------------- | ----------------- |
| Azure         |  [![CircleCI][31]][32] | [![2.0.x][29]][30]  |
| Aws           |  [![GircleCI][19]][20]   |  [![2.0.x][21]][22] |
| GCP           |  [![CircleCI][23]][24]   |  [![2.0.x][25]][26] |
| Openshift/k8s |  [![Gitlab][27]][28]   |        Soon       |

[18]: https://img.shields.io/badge/pipeline-todo-orange
[19]: https://circleci.com/gh/the-maux/tipboard/tree/master.svg?style=svg
[20]: https://circleci.com/gh/the-maux/tipboard/tree/master
[21]: https://img.shields.io/badge/pipeline-todo-orange
[22]: https://img.shields.io/badge/pipeline-todo-orange
[23]: https://circleci.com/gh/the-maux/tipboard/tree/master.svg?style=svg
[24]: https://img.shields.io/badge/pipeline-todo-orange
[25]: https://img.shields.io/badge/pipeline-todo-orange
[26]: https://img.shields.io/badge/pipeline-todo-orange
[27]: https://img.shields.io/badge/pipeline-todo-orange
[28]: https://img.shields.io/badge/pipeline-todo-orange
[29]: https://img.shields.io/badge/pipeline-todo-orange
[30]: https://img.shields.io/badge/pipeline-todo-orange
[31]: https://img.shields.io/badge/pipeline-todo-orange
[32]: https://img.shields.io/badge/pipeline-todo-orange

License
-------

Tipboard is licensed under the [Apache License, v2.0](http://tipboard.readthedocs.org/en/latest/license.html).

Copyright (c) 2013-2017 [Allegro Group](http://allegrogroup.com).

