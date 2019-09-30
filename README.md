  <p align="center">
  <img alt="BetterCap" src="https://i.ibb.co/Fx6FykP/image-5.png"/> 
  <p align="center">
    <a href="http://hits.dwyl.io/themaux/tipboard">
     <img src="http://hits.dwyl.io/themaux/tipboard.svg"></a>
    <a href="">
     <img alt="pypi" src="https://img.shields.io/pypi/dm/tipboard.svg"></a>
    <a href="">
     <img alt="docker" src="https://img.shields.io/docker/pulls/themaux/tipboard"></a>
    <a href="">
  </br>
    <a href="https://github.com/the-maux/tipboard">
     <img alt="Github" src="https://img.shields.io/github/v/release/the-maux/tipboard"></a>
    <a href="https://pypi.org/project/tipboard2.0/">
     <img alt="Pypi" src="https://badge.fury.io/py/tipboard2.0.svg"></a>
  </br>
    <a href="https://aws.amazon.com">
     <img alt="Aws" src="https://codebuild.eu-west-3.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiOXBBZTVtMk5nMmJFcG9vVFlGUVh3cHNoWUFoWXlCVjNjNkd1RE9ZWGtpVlBpazBLaHFKaFpsdXRuamdTc1d4ckNuTSttZnNoNzkwZHNyRUZrbndaaGdvPSIsIml2UGFyYW1ldGVyU3BlYyI6IjNHTnRyekcvWER0Wk1uRW4iLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master"></a>
    <a href="">
     <img alt="Azure" src="https://dev.azure.com/maximerenaud/tipboard/_apis/build/status/the-maux.tipboard?branchName=master"></a>
    <a href="https://travis-ci.com/the-maux/tipboard"> 
      <img alt="Travis" src="https://travis-ci.com/the-maux/tipboard.svg?branch=develop"></a>
    <a href="https://gitlab.com/the-maux/tipboard/pipelines">
     <img src="https://gitlab.com/the-maux/tipboard/badges/master/pipeline.svg" alt="Gitlab"></a>
    <a href="https://tipboard.readthedocs.io/">
     <img alt="ReadTheDocs" src="https://readthedocs.org/projects/tipboard/badge/?version=latest"></a>
</br>
    <a href="">
     <img alt="Code Quality" src="https://api.codeclimate.com/v1/badges/d8974fc0be8e2b0d4c88/maintainability"></a>
    <a href="https://codeclimate.com/github/the-maux/tipboard/maintainability">
     <img alt="Code Coverage" src="https://api.codeclimate.com/v1/badges/d8974fc0be8e2b0d4c88/test_coverage"></a>
    <a href="https://snyk.io//test/github/the-maux/tipboard?targetFile=requirements.txt">
     <img alt="Snyk" src="https://snyk.io//test/github/the-maux/tipboard/badge.svg?targetFile=requirements.txt
"></a>
</p>
</p>

## Introduction

Tipboard is a system for creating dashboards, written in JavaScript and Python.
Its widgets ('tiles' in Tipboard's terminology) are completely
separated from data sources, which provides great flexibility and
relatively high degree of possible customizations.

Because of its intended target (displaying various data and statistics
in your office), it is optimized for larger screens.

A detailed, technical documentation for Tipboard can be found
[here](http://tipboard.readthedocs.org/en/latest/).

#### Continuous.Integration
| :hammer:   |    Runner / Release      |  
| --------   | --------------------- |
| Docs       | ![docs][34] |
| pypi       | [![CircleCI][1]][2] ![][9]  | 
| Github     | [![Gitlab][17]][4] [![Gitlab][3]][4]   |
| DockerHUB  | [![][15]][13] [![][16]][13]        | 
| AWS Code   | [![][33]][13]      |
| AzureBuild | [![][36]][13]         |
| Helm       | [![Gitlab][7]][8]     |

[1]: https://travis-ci.com/the-maux/tipboard.svg?branch=develop
[2]: https://travis-ci.com/the-maux/tipboard
[3]: https://img.shields.io/github/v/release/the-maux/tipboard
[4]: https://github.com/the-maux/tipboard/packages
[5]: https://img.shields.io/badge/pipeline-todo-orange
[6]: https://gitlab.com/the-maux/tipboard/commits/develop
[7]: https://img.shields.io/badge/pipeline-todo-orange
[8]: https://gitlab.com/the-maux/tipboard/commits/develop
[9]: https://badge.fury.io/py/tipboard2.0.svg
[10]: https://pypi.org/project/tipboard2.0/
[11]: https://img.shields.io/docker/stars/themaux/tipboard
[12]: https://pypi.org/project/tipboard2.0/
[13]: https://hub.docker.com/r/themaux/tipboard
[14]: https://img.shields.io/docker/pulls/themaux/tipboard
[15]: https://img.shields.io/docker/cloud/automated/themaux/tipboard
[16]: https://img.shields.io/docker/cloud/build/themaux/tipboard
[17]: https://gitlab.com/the-maux/tipboard/badges/master/pipeline.svg
[33]: https://codebuild.eu-west-3.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiOXBBZTVtMk5nMmJFcG9vVFlGUVh3cHNoWUFoWXlCVjNjNkd1RE9ZWGtpVlBpazBLaHFKaFpsdXRuamdTc1d4ckNuTSttZnNoNzkwZHNyRUZrbndaaGdvPSIsIml2UGFyYW1ldGVyU3BlYyI6IjNHTnRyekcvWER0Wk1uRW4iLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master
[34]: https://readthedocs.org/projects/tipboard/badge/?version=latest
[35]: https://readthedocs.org/projects/tipboard/badge/?version=latest
[36]: https://dev.azure.com/maximerenaud/tipboard/_apis/build/status/the-maux.tipboard?branchName=master


#### Continuous.Deployment
| cloud :cloud: |                     URL / CD-Pipeline                |
| ------------- | ---------------------------------------------------- | 
| Azure         | [![][22]][31] [![AzurePipeline][31]][31]             |
| Aws           | [35.181.91.193][21] [![GircleCI][19]][20]            | 
| GCP           | [tipboard-gcp.appspot.com][29] [![CircleCI][23]][24] | 
| Openshift/k8s | [![Gitlab][27]][28] [![Gitlab][27]][28]              | 

[18]: https://img.shields.io/badge/pipeline-todo-orange
[19]: https://circleci.com/gh/the-maux/tipboard/tree/master.svg?style=svg
[20]: https://circleci.com/gh/the-maux/tipboard/tree/master
[21]: http://35.181.91.193
[22]: https://img.shields.io/badge/pipeline-todo-orange
[23]: https://circleci.com/gh/the-maux/tipboard/tree/master.svg?style=svg
[24]: https://img.shields.io/badge/pipeline-todo-orange
[25]: https://img.shields.io/badge/pipeline-todo-orange
[26]: https://img.shields.io/badge/pipeline-todo-orange
[27]: https://img.shields.io/badge/pipeline-todo-orange
[28]: https://img.shields.io/badge/pipeline-todo-orange
[29]: https://tipboard-gcp.appspot.com/
[30]: https://img.shields.io/badge/pipeline-todo-orange
[31]: https://dev.azure.com/maximerenaud/tipboard/_apis/build/status/tipboard?branchName=master
[32]: https://img.shields.io/badge/pipeline-todo-orange

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

License
-------

Tipboard is licensed under the [Apache License, v2.0](http://tipboard.readthedocs.org/en/latest/license.html).

Copyright (c) 2013-2017 [Allegro Group](http://allegrogroup.com).

