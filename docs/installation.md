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

The scripts directory contains environment preparation and startup helpers for both Linux and Windows.

Fist, run the scripts to prepare the environment.
=== "Linux"

    ```bash
    chmod +x scripts/prepare_environment.sh
    ./scripts/prepare_environment.sh
    ```

=== "Windows (PowerShell)"

    ```powershell
    Set-ExecutionPolicy -Scope Process Bypass
    ./scripts/prepare_environment.ps1
    ```

Then, install the helm chart using your custom values.

```bash
helm install laredo helm-chart/laredo -f <path/to/values.yaml>
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
kubectl apply --server-side --force-conflicts -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml
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
  helm upgrade --install cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --create-namespace \
    --version "1.17.0" \
    --set crds.enabled=true \
    --wait \
    --timeout 10m
```

### 2. KServe CRDs

```bash
helm upgrade --install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
    --version v0.18.0 \
    --namespace kserve \
    --create-namespace
```

### 3. KServe core and runtime configuration

```bash
helm upgrade --install kserve oci://ghcr.io/kserve/charts/kserve-resources \
    --version v0.18.0 \
    --namespace kserve \
    --create-namespace \
    --set kserve.controller.deploymentMode=Standard \
    --set kserve.controller.gateway.ingressGateway.enableGatewayApi=true \
    --set kserve.controller.gateway.ingressGateway.className=nginx \
    --set kserve.controller.gateway.ingressGateway.kserveGateway=laredo/laredo-gateway \
    --set ingress.disableIstioVirtualHost=true \
    --set kserve.controller.gateway.domain="127.0.0.1.nip.io"
```

```bash
helm upgrade --install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs \
    --version v0.18.0 \
    --namespace kserve \
    --create-namespace \
    --set kserve.servingruntime.enabled=true \
    --set kserve.llmisvcConfigs.enabled=false
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
docker pull ghcr.io/istr-uc/laredomlops-trainer-cpu:1.0.2
docker pull ghcr.io/istr-uc/laredomlops-inference-service:1.0.2
docker pull ghcr.io/istr-uc/laredomlops-ollama:1.0.0
docker pull ghcr.io/istr-uc/laredomlops-mlflow:1.0.0
docker pull localstack/localstack:4.14
docekr pull postgres:14
```

If the cluster is Kind, you can also load the images directly into the node:

```bash
kind load docker-image <image-name> --name <cluster-name>
```

## MLflow

If you want to use MLflow inside the cluster, prepare the credentials and connection URL in `values.yaml`. If you already have an external server, you can simply point to it.

## Deployment

Complete the required configuration values and deploy the chart.

```bash
helm install laredo -f <path/to/values.yaml> ./helm-chart/laredo
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
- For a local test deployment, it can also be useful to review [Local deployment](local-deployment.md).
