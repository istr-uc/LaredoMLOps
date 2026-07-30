$ErrorActionPreference = 'Stop'

function Write-Step {
    param([string]$Message)
    Write-Host "[+] $Message" -ForegroundColor Cyan
}

function Assert-Command {
    param([string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

Assert-Command kubectl
Assert-Command helm
Assert-Command docker

Write-Step 'Checking Kubernetes access'
kubectl cluster-info | Out-Null

Write-Step 'Installing Gateway API CRDs'
kubectl apply --server-side --force-conflicts -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.2.0/standard-install.yaml

Write-Step 'Installing cert-manager'
helm upgrade --install cert-manager jetstack/cert-manager `
    --namespace cert-manager `
    --create-namespace `
    --version '1.17.0' `
    --set crds.enabled=true `
    --wait `
    --timeout 10m

Write-Step 'Installing KServe CRDs'
helm upgrade --install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd `
    --version v0.18.0 `
    --namespace kserve `
    --create-namespace

Write-Step 'Installing KServe resources'
helm upgrade --install kserve oci://ghcr.io/kserve/charts/kserve-resources `
    --version v0.18.0 `
    --namespace kserve `
    --create-namespace `
    --set kserve.controller.deploymentMode=Standard `
    --set kserve.controller.gateway.ingressGateway.enableGatewayApi=true `
    --set kserve.controller.gateway.ingressGateway.className=nginx `
    --set kserve.controller.gateway.ingressGateway.kserveGateway=laredo/laredo-gateway `
    --set ingress.disableIstioVirtualHost=true `
    --set kserve.controller.gateway.domain='127.0.0.1.nip.io'

Write-Step 'Installing KServe runtime configs'
helm upgrade --install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs `
    --version v0.18.0 `
    --namespace kserve `
    --create-namespace `
    --set kserve.servingruntime.enabled=true `
    --set kserve.llmisvcConfigs.enabled=false

$skipImagePull = $env:SKIP_IMAGE_PULL -eq '1'
if (-not $skipImagePull) {
    $images = @(
        'ghcr.io/istr-uc/laredomlops-trainer-cpu:1.0.2',
        'ghcr.io/istr-uc/laredomlops-frontend:1.1.0',
        'ghcr.io/istr-uc/laredomlops-backend:1.1.0',
        'ghcr.io/istr-uc/laredomlops-ollama:1.0.0',
        'ghcr.io/istr-uc/laredomlops-chatbot:1.0.0',
        'ghcr.io/istr-uc/laredomlops-mlflow:1.0.0',
        'ghcr.io/istr-uc/laredomlops-inference-service:1.0.2',
        'localstack/localstack:4.14',
        'postgres:14'
    )

    foreach ($image in $images) {
        Write-Step "Pulling Docker image $image"
        docker pull $image
    }
} else {
    Write-Host '[+] Skipping image pulls because SKIP_IMAGE_PULL=1' -ForegroundColor Yellow
}

Write-Host '[+] Environment preparation complete.' -ForegroundColor Green
