# Installation guide

This guide will provide you with the necessary steps to install and configure all the components required to run Laredo. Follow the instructions in the order presented to ensure a successful installation.

## 1. Docker Installation

Docker allows you to encapsulate applications into lightweight containers, facilitating management and deployment.

Steps:

Download Docker Desktop from the official website.
[Windows installation](https://docs.docker.com/desktop/setup/install/windows-install/) or [Linux Installation](https://docs.docker.com/desktop/setup/install/linux/)



## 2. Kind Installation

Purpose: Kind allows you to run a local Kubernetes cluster. Ideal for testing.

Steps:

Open a shell as an administrator.

Run the following command to install Kind using Winget: 
```powershell
winget install Kubernetes.kind
```
On linux run:
```bash
[ $(uname -m) = x86_64 ] && curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.30.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```


## 3. Kubectl Installation

Kubectl is the command-line tool for interacting with Kubernetes clusters.

Steps:

Open shell as an administrator.

Run the following command to install Kubectl using Winget:
```powershell
winget install -e --id Kubernetes.kubectl
```
On Linux run:
```bash
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## 4. Helm Installation

Helm is a package manager for Kubernetes, simplifying application deployment and management. We use helm to simplify the installation and configuration of the different components that comprise Laredo.

Steps:

Open a shell as an administrator.

On Windows run the following command: 
```powershell
winget install Helm.Helm
```
On Linux based OS run:

```bash
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ ./get_helm.sh
```


## 5. Seldon Core Installation

Purpose: Seldon Core is a platform for deploying machine learning models on Kubernetes.

Steps:

Follow the official Seldon Core installation guide up to the "Set up Kind" section:  (if there is no installation steps, follow the next steps)

Create a Kind cluster for local deployment: 

```
kind create cluster --name seldon
```
or

Use connect to an already available kubernetes cluster

Verify the cluster: kubectl cluster-info --context kind-seldon

Install Istio:

- Download the latest Istio release from the Istio releases page.

- Extract the downloaded file and add the bin directory path to your system's PATH environment variable.

- Verify the Istio installation: `istioctl version`

Continue with the Seldon Core installation:
```bash
kubectl label namespace default istio-injection=enabled

istioctl install --set profile=demo -y

kubectl apply -f seldon-gateway.yaml (the provided yaml file).

kubectl create namespace seldon-system

helm install seldon-core seldon-core-operator  --repo https://storage.googleapis.com/seldon-charts --set usageMetrics.enabled=true --set istio.enabled=true --namespace seldon-system
```
Verify the pods: `kubectl get pods -n seldon-system`

## 6. Istio Installation

Purpose: Istio is a service mesh that manages network traffic between microservices.

Steps: Already installed in step 5.

Verification: `kubectl get pods -n istio-system`

Expose the Istio gateway (local deployment): 
```bash
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80 #(run in a separate terminal).
```
## 7. MLflow Installation

You can install an MLFlow server on your kubernetes cluster for testing purposes by letting the MLflow connection configuration empty on the values.yaml.


## 8. Laredo Installation

Create a new values.yaml file with the parameters needed and install with:
```bash
helm install laredo  -f “valueslaredocmind.yaml” oci://ghcr.io/dintenr/laredo --version 0.1.0
```