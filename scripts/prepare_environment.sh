#!/usr/bin/env bash
set -euo pipefail

log() {
  echo "[+] $*"
}

fail() {
  echo "[x] $*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

run_step() {
  local description="$1"
  shift
  log "$description"
  "$@"
}

SKIP_IMAGE_PULL="${SKIP_IMAGE_PULL:-0}"

require_cmd kubectl
require_cmd helm
require_cmd docker

log "Checking Kubernetes access"
kubectl cluster-info >/dev/null 2>&1 || fail "Kubernetes cluster is not reachable. Is Docker Desktop or your cluster running?"

run_step "Installing Gateway API CRDs" \
  kubectl apply --server-side --force-conflicts -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

run_step "Installing cert-manager" \
  helm upgrade --install cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --create-namespace \
    --version "1.17.0" \
    --set crds.enabled=true \
    --wait \
    --timeout 10m

run_step "Installing KServe CRDs" \
  helm upgrade --install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
    --version v0.18.0 \
    --namespace kserve \
    --create-namespace

run_step "Installing KServe resources" \
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

run_step "Installing KServe runtime configs" \
  helm upgrade --install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs \
    --version v0.18.0 \
    --namespace kserve \
    --create-namespace \
    --set kserve.servingruntime.enabled=true \
    --set kserve.llmisvcConfigs.enabled=false

if [[ "$SKIP_IMAGE_PULL" != "1" ]]; then
  images=(
    ghcr.io/istr-uc/laredomlops-trainer-cpu:1.0.2
    ghcr.io/istr-uc/laredomlops-frontend:1.1.0
    ghcr.io/istr-uc/laredomlops-backend:1.1.0
    ghcr.io/istr-uc/laredomlops-ollama:1.0.0
    ghcr.io/istr-uc/laredomlops-chatbot:1.0.0
    ghcr.io/istr-uc/laredomlops-mlflow:1.0.0
    ghcr.io/istr-uc/laredomlops-inference-service:1.0.2
    localstack/localstack:4.14
    postgres:14
  )

  for image in "${images[@]}"; do
    run_step "Pulling Docker image $image" docker pull "$image"
  done
else
  log "Skipping image pulls because SKIP_IMAGE_PULL=1"
fi

log "Environment preparation complete."
