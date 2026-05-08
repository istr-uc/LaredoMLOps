# LaredoMLOps Start-up Script for Local Development (Docker Desktop)

Write: This script automates the environment setup, deployment, and local access configuration for LaredoMLOps.

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting LaredoMLOps deployment..." -ForegroundColor Cyan

# 1. Validate Environment
Write-Host "🔍 Validating environment..." -ForegroundColor Cyan
try {
    kubectl cluster-info | Out-Null
    Write-Host "✅ Kubernetes cluster is reachable." -ForegroundColor Green
} catch {
    Write-Error "❌ Kubernetes cluster is not reachable. Is Docker Desktop running with Kubernetes enabled?"
    exit 1
}

# 2. Install Gateway API CRDs
Write-Host "📦 Installing Gateway API CRDs..." -ForegroundColor Cyan
try {
    # Using a stable version of the Gateway API CRDs
    kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.0.0/standard-install.yaml
    Write-Host "✅ Gateway API CRDs applied." -ForegroundColor Green
} catch {
    Write-Error "❌ Failed to apply Gateway API CRDs."
    exit 1
}

# 3. Deploy via Helm
$chartPath = "../helm-chart/laredo"
if (-not (Test-Path -Path $chartPath)) {
    Write-Error "❌ Helm chart not found at $chartPath. Please run this script from the 'scripts' directory."
    exit 1
}

Write-Host "☸️ Deploying LaredoMLOps via Helm..." -ForegroundColor Cyan
try {
    helm upgrade --install laredo $chartPath `
        --namespace laredo `
        --create-namespace `
        --values $chartPath/values.yaml
    Write-Host "✅ Helm deployment initiated." -ForegroundColor Green
} catch {
    Write-Error "❌ Helm deployment failed."
    exit 1
}

# 4. Wait for Backend Readiness
Write-Host "⏳ Waiting for backend deployment to be available..." -ForegroundColor Cyan
try {
    kubectl wait --for=condition=available deployment/laredo-backend -n laredo --timeout=120s
    Write-Host "✅ Backend is ready!" -ForegroundColor Green
} catch {
    Write-Error "❌ Backend deployment failed to become available within timeout."
    exit 1
}

# 5. Setup Port Forwarding for Gateway
Write-Host "🔌 Setting up port forwarding for the Gateway..." -ForegroundColor Cyan
try {
    # We attempt to forward the service that handles the gateway traffic (usually the backend or an ingress/gateway service)
    # The gateway routes traffic to the laredo-frontend and laredo-backend services.
    # To allow access via localhost, we will forward the laredo-frontend service.
    
    $portForwardProcess = Start-Process kubectl -ArgumentList "port-forward svc/nginx-gateway-nginx-gateway-fabric -n nginx-gateway 80:80 -n laredo" -WindowStyle Hidden -PassThru
    
    Write-Host "✅ Port forwarding started in the background (mapping localhost:80 -> laredo-frontend)." -ForegroundColor Green
    Write-Host "`n✨ LaredoMLOps is ready for your usability test!" -ForegroundColor White -BackgroundColor DarkGreen
    Write-Host "🔗 Access the application at: http://app.127.0.0.1.nip.io:80" -ForegroundColor White
    Write-Host "`n(To stop the script and port-forwarding, close this terminal or kill the kubectl process.)" -ForegroundColor Gray

} catch {
    Write-Error "❌ Failed to start port forwarding."
    exit 1
}
