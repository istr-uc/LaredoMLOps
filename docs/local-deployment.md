# Local deployment and default values

The default values in the `values.yaml` file are primarily intended to bring up a local test environment with the least effort possible. For that reason, the chart is prepared to work with simple and accessible components such as:

- local S3 storage using LocalStack
- internal PostgreSQL for testing
- integrated MLflow
- services using the `ClusterIP` type
- local hosts such as `*.127.0.0.1.nip.io`
- a single replica and horizontal scaling disabled

This approach allows you to validate the application quickly, but it is not intended for production.

## What the default values are for

The default values are meant to:

- test the full deployment without needing additional infrastructure preparation
- validate the integration between the backend, frontend, and chatbot
- run the stack in a local cluster or development environment
- reduce the number of overrides required at the start

In this sense, example values such as `admin123`, `test`, or `your-google-api-key` are acceptable for testing, but they should be changed if the deployment is used outside the local environment.

## Parameters that usually do not need to be changed for local testing

These values are generally suitable as-is for an initial deployment:

- `backend.deploy_s3_storage`
- `backend.deploy_postgres`
- `backend.deploy_mlflow`
- `backend.s3_service_port`
- `backend.postgres_service_port`
- `backend.mlflow_tracking_uri_ip`
- `backend.mlflow_tracking_uri_port`
- `gatewayAPI.enabled`
- `autoscaling.enabled`
- `backend.replicaCount`, `frontend.replicaCount`, `chatbotBackend.replicaCount`

## Parameters worth changing

There are no strictly mandatory parameters for local deployment to work, because the defaults already allow the stack to start. However, there are several values worth changing depending on the use case.

### Parameters that are required or almost required for an environment other than local

These should be updated if you want to use your own images, real credentials, or a different access model:

- `backend.image.repository` and `backend.image.tag`
- `frontend.image.repository` and `frontend.image.tag`
- `chatbotBackend.image.repository` and `chatbotBackend.image.tag`
- `backend.postgres_admin_password`
- `backend.postgres_password`
- `backend.AWS_ACCESS_KEY_ID`
- `backend.AWS_SECRET_ACCESS_KEY`
- `chatbotBackend.api_keys.GOOGLE_API_KEY`
- `chatbotBackend.api_keys.LANGSMITH_API_KEY`
- `chatbotBackend.llm_models.*` if you want to change the models used

### Optional but recommended parameters for adjusting the deployment

These are not required for the stack to work, but they do improve the result depending on the environment:

- `backend.service.type` to change `ClusterIP` to `NodePort` or `LoadBalancer`
- `gatewayAPI.hosts.*` if you want to use different hostnames or paths
- `resources.requests` and `resources.limits` to adjust CPU and memory
- `autoscaling.minReplicas`, `autoscaling.maxReplicas`, and `autoscaling.targetCPUUtilizationPercentage`
- `volumes` and `volumeMounts` if you need persistence or additional mounts
- `nodeSelector`, `tolerations`, and `affinity` to control pod placement

## Practical recommendation

For a first local test, the simplest approach is to leave the default values as they are. If the deployment will be used more seriously or in a shared environment, it is worth reviewing the following first:

1. images and tags
2. credentials and secrets
3. hostnames and service exposure
4. resources and scaling

This combination usually covers most of the changes needed without having to touch the rest of the chart.
