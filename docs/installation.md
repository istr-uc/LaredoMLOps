# Installation

This guide summarizes the current installation process for preparing the environment and deploying Laredo.

## Prerequisites

- A Kubernetes cluster available.
- Docker or a compatible container runtime.
- `kubectl` available to manage the cluster.
- Helm installed.
- Access to an MLflow server if you want to use an external one.
- A `values.yaml` file with environment-specific parameters.

## Before you start

If you want to validate the installation locally, the recommended flow is to install Docker first, then Kind, and finally the Kubernetes tools.

## Recommended workflow

1. Install Docker Desktop or the container runtime you use locally.
2. Install Kind if you want to test on a local cluster.
3. Install `kubectl` to interact with Kubernetes.
4. Install Helm to deploy the Laredo chart.
5. Install NGINX Gateway Fabric as the cluster ingress gateway.
6. Install cert-manager and the KServe CRDs.
7. Install KServe and the KServe runtime configuration.
8. Pre-pull the stack images to speed up chart deployment.
9. Complete the `values.yaml` file.
10. Deploy the chart and review the pods.

## Using script

The scripts directory contains installation and startup helpers for both Linux and Windows.

=== "Linux"

    ```bash
    chmod +x scripts/start-laredo.sh
    ./scripts/start-laredo.sh
    ```

=== "Windows (PowerShell)"

    ```powershell
    Set-ExecutionPolicy -Scope Process Bypass
    ./scripts/start-laredo.ps1
    ```

If you prefer, you can follow the next steps manually instead.

## Installing dependencies

### Docker

Docker packages applications into lightweight containers to simplify management and deployment.

### Kind

Kind lets you run a local Kubernetes cluster for testing.

```powershell
winget install Kubernetes.kind
```

### kubectl

`kubectl` is the command-line tool for interacting with Kubernetes.

```powershell
winget install -e --id Kubernetes.kubectl
```

### Helm

Helm is used to install and update Laredo through its chart.

```powershell
winget install Helm.Helm
```

## NGINX Gateway Fabric

NGINX Gateway Fabric provides the ingress gateway used by the chart to expose services from the cluster.

```bash
kubectl apply -f https://github.com/nginxinc/nginx-gateway-fabric/releases/latest/download/nginx-gateway-fabric.yaml
```

Quick verification:

```bash
kubectl get pods -n nginx-gateway
kubectl get gatewayclass
```

## KServe

KServe is installed in several stages to prepare the inference environment.

### 1. Cert-manager

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml
```

### 2. KServe CRDs

```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.15.0/kserve.yaml
```

### 3. KServe core and runtime configuration

```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.15.0/kserve-runtimes.yaml
```

### 4. Verification

```bash
kubectl get pods -n cert-manager
kubectl get pods -n kserve
```

## Pre-pulling images

To speed up chart deployment, it is a good idea to pre-load the images that the stack will use in your local environment. This avoids long waits when the pods start for the first time.

Example preload for a local environment:

```bash
docker pull ghcr.io/istr-uc/laredomlops-backend:1.1.0
docker pull ghcr.io/istr-uc/laredomlops-frontend:1.1.0
docker pull ghcr.io/istr-uc/laredomlops-chatbot:1.0.0
docker pull ghcr.io/istr-uc/laredomlops-trainer-cpu:1.0.1
docker pull ghcr.io/istr-uc/laredomlops-inference-service:1.1.0
```

If the cluster is Kind, you can also load the images directly into the node:

```bash
kind load docker-image ghcr.io/istr-uc/laredomlops-backend:1.1.0 --name <cluster-name>
kind load docker-image ghcr.io/istr-uc/laredomlops-frontend:1.1.0 --name <cluster-name>
kind load docker-image ghcr.io/istr-uc/laredomlops-chatbot:1.0.0 --name <cluster-name>
kind load docker-image ghcr.io/istr-uc/laredomlops-trainer-cpu:1.0.1 --name <cluster-name>
kind load docker-image ghcr.io/istr-uc/laredomlops-inference-service:1.1.0 --name <cluster-name>
```

## MLflow

If you want to use MLflow inside the cluster, prepare the credentials and connection URL in `values.yaml`. If you already have an external server, you can simply point to it.

## Deployment

Complete the required configuration values and deploy the chart.

```bash
helm install laredo -f values.yaml ./helm-chart/laredo
```

After deployment, check the pods and verify that the gateway and KServe services are available.

## Checks

```bash
kubectl get pods
kubectl get gatewayclass
kubectl get pods -n cert-manager
kubectl get pods -n kserve
kubectl cluster-info
```

## Practical notes

- If you are not yet clear on the configuration in `values.yaml`, review the [Configuration](configuration.md) page.
- If you want to show the process with screenshots or a short video, use the [Multimedia](multimedia.md) page.
- For a local test deployment, it can also be useful to review [Local deployment](local-deployment.md).
