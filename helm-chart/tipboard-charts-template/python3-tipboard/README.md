# Python3.7 Tipboard

python3-tipboard

# Introduction

This chart bootstraps applications based on Python Django in openshift.

## Configuration

You have to create an image pull secrets manually in your namespace to pull the docker image and set the imagePullSecrets array with your registries credentials.

The following table lists the configurable parameters of the Spring cloud config server chart and their default values.

| Parameter | Description | Default |
| - | - | - |
| `app` | the resource names | python-django |
| `image` | image registry and name | None |
| `version` | image version | latest |
| `imagePullSecrets` | an array of secrets for pull private image registries | None |
| `env` | an array of container environment variables | None |
| `secretData` | group of secret data | None |
| `configMaps` | an arrays of config maps to attach to pods | None |
| `ingressHostDomain` | ingress host domain when you want to use an ingress route instead of an openshift route | None |
| `podAnnotations` | yaml pod annotations for the pod | See default values.yaml file |
| `replicas` | the number of replicas to run | 1 |
| `readinessProbePath` | readiness probe path | /health |
| `cpuRequest` | cpu request | 100m |
| `memoryRequest` | memory request | 256Mi |
| `cpuLimit` | cpu limit | 100m |
| `memoryLimit` | memory limit | 256Mi |
| `volumeName` | name of data volume | None |
| `volumeCapacity` | size of data volume | 1Gi |
| `mountPath` | Path Route ingressHostDomain | None |
