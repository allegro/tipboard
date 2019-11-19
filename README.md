  <p align="center">
  <img alt="Tipboard" src="https://i.ibb.co/Fx6FykP/image-5.png"/>
  <p align="center">
    <a href="https://gitter.im/tipboard-dev/community">
     <img alt="Chat" src="https://img.shields.io/gitter/room/DAVFoundation/DAV-Contributors.svg?style=flat-square"></a>
    <a href="https://github.com/the-maux/tipboard">
     <img alt="Github" src="https://img.shields.io/github/v/release/the-maux/tipboard"></a>
    <a href="https://pypi.org/project/tipboard2.0/">
     <img alt="Pypi" src="https://badge.fury.io/py/tipboard2.0.svg"></a>
</br>
    <a href="https://allegro.tech/tipboard/">
     <img src="http://hits.dwyl.io/themaux/tipboard.svg"></a>
    <a href="">
     <img alt="pypi" src="https://img.shields.io/pypi/dm/tipboard.svg"></a>
    <a href="">
     <img alt="docker" src="https://img.shields.io/docker/pulls/themaux/tipboard"></a>
    <a href="">
</br>
    <a href="https://travis-ci.com/the-maux/tipboard">
      <img alt="Travis" src="https://travis-ci.com/the-maux/tipboard.svg?branch=develop"></a>
    <a href="https://gitlab.com/the-maux/tipboard/pipelines">
     <img src="https://gitlab.com/the-maux/tipboard/badges/master/pipeline.svg" alt="Gitlab"></a>
    <a href="https://tipboard.readthedocs.io/">
     <img alt="ReadTheDocs" src="https://readthedocs.org/projects/tipboard/badge/?version=latest"></a>  
</br>
<a href="https://codebeat.co/projects/github-com-the-maux-tipboard-develop"><img alt="codebeat badge" src="https://codebeat.co/badges/9505d595-5b06-46bb-b7c6-1623090fc2f5" /></a>
    <a href="">
     <img alt="Code Quality" src="https://api.codeclimate.com/v1/badges/d8974fc0be8e2b0d4c88/maintainability"></a>
    <a href="https://codeclimate.com/github/the-maux/tipboard/maintainability">
     <img alt="Codacy" src="https://api.codacy.com/project/badge/Grade/b28af36f50584bd29612b66bc42ce0c3"></a>
</br>
    <a href="https://semaphoreci.com/the-maux/tipboard">
     <img alt="Semaphore" src="https://semaphoreci.com/api/v1/the-maux/tipboard/branches/wip/badge.svg"></a>
    <img alt="Code Coverage" src="https://api.codeclimate.com/v1/badges/d8974fc0be8e2b0d4c88/test_coverage"></a>
     <a href="https://www.codacy.com/manual/the-maux/tipboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=the-maux/tipboard&amp;utm_campaign=Badge_Grade">
</br>
    <a href="https://snyk.io/test/github/the-maux/tipboard?targetFile=requirements.txt">
     <img alt="Snyk" src="https://snyk.io/test/github/the-maux/tipboard/badge.svg?targetFile=requirements.txt"></a>
     <a href="https://pyup.io/account/repos/github/the-maux/tipboard/">
    <img alt="PyUp" src="https://pyup.io/repos/github/the-maux/tipboard/shield.svg"></a>

</br>
</p>
</p>

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

C.I / C.D
---------

#### Continuous.Integration

| C.I :hammer:     |    Stages                               |
| -------------    | --------------------------------------- |
| Travis           |  [![Build Status][1]][2]                |
| CodeFresh        |  [![Codefresh build status][3]][4]      |
| CircleCI         |  [![GircleCI][19]][20]                  |
| Pyup/safety-ci   |  ![Pyup][9]                             |
| Scrutinizer      |  [![Scrutinizer Code Quality][5]][6]    |
| DockerCI         | ![Docker][7] ![Docker][8]               |
| AzureBuild       | [![AzurePipeline][31]][31]              |
| AwsCodeBuild     | ![][33]                                 |
| Codacy           | [![Codacy Badge][10]][11]               |
| HelmChart        | ![][24]                                 |
| GoogleCloudBuild |  :x:                                    |

#### Continuous.Deployment
| cloud :cloud: |                     URL / CD-Pipeline      |
| ------------- | ------------------------------------------ |
| Azure         | [![AzurePipeline][31]][31] [![][22]][31]   |
| Aws           | ![][33] [![GircleCI][19]][20]              |
| GCP           | [![CircleCI][23]][24]                      |
| Openshift/k8s | [![Gitlab][27]][28] [![Gitlab][27]][28]    |

License
-------

Tipboard is licensed under the [Apache License, v2.0](http://tipboard.readthedocs.org/en/latest/license.html).

Copyright (c) 2013-2017 [Allegro Group](http://allegrogroup.com).

[1]: https://travis-ci.com/the-maux/tipboard.svg?branch=develop
[2]: https://travis-ci.com/the-maux/tipboard
[3]: https://g.codefresh.io/api/badges/pipeline/themaux/tipboard%2FMyPipeline?key=eyJhbGciOiJIUzI1NiJ9.NWQ5NDkxYzg1YzI5YzVmOWQyODQ0MDc4.rDj-1Rn5DxSkv_oE8p87ijZhoTelE_WjvbbKWMCI3ZA&type=cf-1
[4]: https://g.codefresh.io/pipelines/MyPipeline/builds?filter=trigger:build~Build;pipeline:5d9492f4941e460201d39d0a~MyPipeline
[5]: https://scrutinizer-ci.com/g/the-maux/tipboard/badges/quality-score.png?b=develop
[6]: https://scrutinizer-ci.com/g/the-maux/tipboard/?branch=develop
[7]: https://img.shields.io/docker/cloud/build/themaux/tipboard
[8]: https://img.shields.io/microbadger/image-size/themaux/tipboard/latest
[9]: https://pyup.io/repos/github/the-maux/tipboard/shield.svg
[10]: https://api.codacy.com/project/badge/Grade/b28af36f50584bd29612b66bc42ce0c3
[11]: https://www.codacy.com/manual/the-maux/tipboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=the-maux/tipboard&amp;utm_campaign=Badge_Grade
[18]: https://img.shields.io/badge/pipeline-todo-orange
[19]: https://circleci.com/gh/the-maux/tipboard/tree/master.svg?style=svg
[20]: https://circleci.com/gh/the-maux/tipboard/tree/master
[22]: https://img.shields.io/badge/pipeline-todo-orange
[23]: https://circleci.com/gh/the-maux/tipboard/tree/master.svg?style=svg
[24]: https://img.shields.io/badge/pipeline-todo-orange
[25]: https://img.shields.io/badge/pipeline-todo-orange
[26]: https://img.shields.io/badge/pipeline-todo-orange
[27]: https://img.shields.io/badge/pipeline-todo-orange
[28]: https://img.shields.io/badge/pipeline-todo-orange
[31]: https://dev.azure.com/maximerenaud/tipboard/_apis/build/status/tipboard?branchName=master
[33]: https://codebuild.eu-west-3.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiOXBBZTVtMk5nMmJFcG9vVFlGUVh3cHNoWUFoWXlCVjNjNkd1RE9ZWGtpVlBpazBLaHFKaFpsdXRuamdTc1d4ckNuTSttZnNoNzkwZHNyRUZrbndaaGdvPSIsIml2UGFyYW1ldGVyU3BlYyI6IjNHTnRyekcvWER0Wk1uRW4iLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master
