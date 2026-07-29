# Configuration

This page acts as a reference for all configurable parameters in the Helm chart `values.yaml` file.

> To better understand the purpose of the default values and what should be modified for a local test deployment, see the [Local deployment](local-deployment.md) page.

## General parameters

| Parameter | Description | Example |
| --- | --- | --- |
| `resources` | Global block for requested resources and limits per pod. | `requests.cpu: 100m` |
| `autoscaling.enabled` | Enables horizontal autoscaling. | `true` |
| `volumes` | Additional volumes to attach to deployments. | `secret` |
| `volumeMounts` | Additional volume mounts. | `/etc/foo` |
| `nodeSelector` | Constraints for scheduling pods on specific nodes. | `{disktype: ssd}` |
| `tolerations` | Tolerations for scheduling pods on tainted nodes. | `[]` |
| `affinity` | Affinity and anti-affinity rules. | `{}` |

## Backend

| Parameter | Description | Example |
| --- | --- | --- |
| `backend.replicaCount` | Number of backend replicas. | `1` |
| `backend.namespace` | Namespace where the component will be deployed. | `laredo` |
| `backend.image.repository` | Backend image repository. | `ghcr.io/istr-uc/laredomlops-backend` |
| `backend.image.pullPolicy` | Image pull policy. | `IfNotPresent` |
| `backend.image.tag` | Backend image tag. | `1.1.0` |
| `backend.imagePullSecrets` | Secrets for pulling private images. | `[]` |
| `backend.nameOverride` | Override for the base resource name. | `""` |
| `backend.fullnameOverride` | Override for the full resource name. | `""` |
| `backend.serviceAccount.create` | Creates a dedicated service account. | `true` |
| `backend.serviceAccount.automount` | Automatically mounts the service account token. | `true` |
| `backend.serviceAccount.annotations` | Service account annotations. | `{}` |
| `backend.serviceAccount.name` | Explicit name for the service account. | `""` |
| `backend.podAnnotations` | Pod annotations. | `{}` |
| `backend.podLabels` | Pod labels. | `{}` |
| `backend.podSecurityContext` | Pod security context. | `{}` |
| `backend.securityContext` | Container security context. | `{}` |
| `backend.service.name` | Service name. | `laredo-backend` |
| `backend.service.type` | Service type. | `ClusterIP` |
| `backend.service.port` | Service port. | `5050` |
| `backend.deploy_s3_storage` | Enables deployment of S3-compatible storage using LocalStack. | `true` |
| `backend.s3_storage_size` | Size of the S3 storage volume. | `10Gi` |
| `backend.s3_service_port` | Port of the LocalStack service. | `4566` |
| `backend.deploy_postgres` | Enables deployment of PostgreSQL. | `true` |
| `backend.postgres_admin_password` | PostgreSQL administrator password. | `admin123` |
| `backend.postgres_service_port` | PostgreSQL service port. | `5432` |
| `backend.postgres_storage_size` | Size of the PostgreSQL volume. | `10Gi` |
| `backend.deploy_mlflow` | Enables deployment of MLflow. | `true` |
| `backend.mlflow_tracking_uri_ip` | Host/IP of the MLflow server. | `mlflow-service` |
| `backend.mlflow_tracking_uri_port` | Port of the MLflow server. | `5000` |
| `backend.mlflow_externalStorage` | Uses external storage for MLflow artifacts. | `true` |
| `backend.mlflow_artifact_uri` | MLflow artifact URI. | `s3://mlflow-artifacts/artifacts` |
| `backend.postgres_db_name` | Database name for MLflow. | `mlflow` |
| `backend.postgres_user` | PostgreSQL username. | `postgres` |
| `backend.postgres_password` | PostgreSQL password. | `admin123` |
| `backend.postgres_host` | PostgreSQL host. | `postgres` |
| `backend.postgres_port` | PostgreSQL port. | `5432` |
| `backend.S3_INTERNAL_ENDPOINT_URL` | Internal S3 endpoint inside the cluster. | `http://localstack-service:4566` |
| `backend.MLFLOW_S3_ENDPOINT_URL` | External endpoint for S3 access. | `http://localstack.127.0.0.1.nip.io` |
| `backend.AWS_ACCESS_KEY_ID` | Access key for AWS/S3 credentials. | `test` |
| `backend.AWS_SECRET_ACCESS_KEY` | Secret key for AWS/S3 credentials. | `test` |
| `backend.AWS_DEFAULT_REGION` | Default AWS region. | `us-east-1` |
| `backend.DATASET_BUCKET_NAME` | Dataset bucket. | `ml-datasets` |
| `backend.TRAINER_IMAGE` | Trainer component image. | `ghcr.io/istr-uc/laredomlops-trainer-cpu` |
| `backend.TRAINER_TAG` | Trainer image tag. | `1.0.1` |
| `backend.INFERENCE_SERVICE_IMAGE` | Inference service image. | `ghcr.io/istr-uc/laredomlops-inference-service` |
| `backend.INFERENCE_SERVICE_TAG` | Inference service image tag. | `1.1.0` |

## Frontend

| Parameter | Description | Example |
| --- | --- | --- |
| `frontend.replicaCount` | Number of frontend replicas. | `1` |
| `frontend.namespace` | Namespace where the frontend is deployed. | `laredo` |
| `frontend.image.repository` | Frontend image repository. | `ghcr.io/istr-uc/laredomlops-frontend` |
| `frontend.image.pullPolicy` | Image pull policy. | `IfNotPresent` |
| `frontend.image.tag` | Frontend image tag. | `1.1.0` |
| `frontend.imagePullSecrets` | Secrets for private images. | `[]` |
| `frontend.nameOverride` | Override for the base resource name. | `""` |
| `frontend.fullnameOverride` | Override for the full resource name. | `""` |
| `frontend.serviceAccount.create` | Creates a dedicated service account. | `true` |
| `frontend.serviceAccount.automount` | Automatically mounts the service account token. | `true` |
| `frontend.serviceAccount.annotations` | Service account annotations. | `{}` |
| `frontend.serviceAccount.name` | Explicit name for the service account. | `""` |
| `frontend.podAnnotations` | Pod annotations. | `{}` |
| `frontend.podLabels` | Pod labels. | `{}` |
| `frontend.podSecurityContext` | Pod security context. | `{}` |
| `frontend.securityContext` | Container security context. | `{}` |
| `frontend.service.name` | Service name. | `laredo-frontend` |
| `frontend.service.type` | Service type. | `ClusterIP` |
| `frontend.service.port` | Service port. | `80` |

## Chatbot backend

| Parameter | Description | Example |
| --- | --- | --- |
| `chatbotBackend.replicaCount` | Number of chatbot backend replicas. | `1` |
| `chatbotBackend.namespace` | Namespace where it is deployed. | `laredo` |
| `chatbotBackend.image.repository` | Chatbot image repository. | `ghcr.io/istr-uc/laredomlops-chatbot` |
| `chatbotBackend.image.pullPolicy` | Image pull policy. | `IfNotPresent` |
| `chatbotBackend.image.tag` | Chatbot image tag. | `1.0.0` |
| `chatbotBackend.imagePullSecrets` | Secrets for private images. | `[]` |
| `chatbotBackend.nameOverride` | Override for the base resource name. | `""` |
| `chatbotBackend.fullnameOverride` | Override for the full resource name. | `""` |
| `chatbotBackend.serviceAccount.create` | Creates a dedicated service account. | `true` |
| `chatbotBackend.serviceAccount.automount` | Automatically mounts the service account token. | `true` |
| `chatbotBackend.serviceAccount.annotations` | Service account annotations. | `{}` |
| `chatbotBackend.serviceAccount.name` | Explicit name for the service account. | `""` |
| `chatbotBackend.podAnnotations` | Pod annotations. | `{}` |
| `chatbotBackend.podLabels` | Pod labels. | `{}` |
| `chatbotBackend.podSecurityContext` | Pod security context. | `{}` |
| `chatbotBackend.securityContext` | Container security context. | `{}` |
| `chatbotBackend.service.name` | Service name. | `laredo-chatbot-backend` |
| `chatbotBackend.service.type` | Service type. | `ClusterIP` |
| `chatbotBackend.service.port` | Service port. | `20000` |
| `chatbotBackend.api_keys.GOOGLE_API_KEY` | Google API key. | `your-google-api-key` |
| `chatbotBackend.api_keys.LANGSMITH_API_KEY` | LangSmith API key. | `your-langsmith-api-key` |
| `chatbotBackend.api_keys.LANGSMITH_TRACING_V2` | Enables LangSmith tracing. | `true` |
| `chatbotBackend.api_keys.LANGSMITH_PROJECT` | LangSmith project. | `chatbot` |
| `chatbotBackend.llm_models.MAIN_LLM_MODEL` | Main LLM model. | `gemma-3-27b-it` |
| `chatbotBackend.llm_models.EMBEDDINGS_MODEL` | Embeddings model. | `gemini-embedding-001` |
| `chatbotBackend.llm_models.LLM_TRANSLATION_SUMMARIZATION_MODEL` | Model for translation and summarization. | `gemma-3-27b-it` |

## Gateway API

| Parameter | Description | Example |
| --- | --- | --- |
| `gatewayAPI.enabled` | Enables Gateway API configuration. | `true` |
| `gatewayAPI.gatewayClassName` | Name of the gateway class. | `nginx` |
| `gatewayAPI.controller.env` | Controller environment variables. | `CLIENT_MAX_BODY_SIZE=0` |
| `gatewayAPI.gateway.name` | Gateway name. | `laredo-gateway` |
| `gatewayAPI.gateway.hostname` | Base gateway hostname. | `127.0.0.1.nip.io` |
| `gatewayAPI.gateway.listeners` | Gateway listeners. | `port: 80` |
| `gatewayAPI.hosts.localstack.*` | LocalStack host configuration. | `service: localstack-service` |
| `gatewayAPI.hosts.mlflow.*` | MLflow host configuration. | `service: mlflow-service` |
| `gatewayAPI.hosts.frontend.*` | Frontend host configuration. | `service: laredo-frontend` |
| `gatewayAPI.corsPolicy.enabled` | Enables CORS policies for Gateway API. | `true` |
| `gatewayAPI.corsPolicy.allowMethods` | Allowed HTTP methods. | `GET, PUT, POST, DELETE, OPTIONS` |
| `gatewayAPI.corsPolicy.allowHeaders` | Allowed headers. | `Authorization` |
| `gatewayAPI.corsPolicy.allowOrigin` | Allowed origin. | `*` |
| `gatewayAPI.corsPolicy.exposeHeaders` | Exposed headers. | `ETag` |

## Resources, scaling, and additional storage

| Parameter | Description | Example |
| --- | --- | --- |
| `resources.limits` | CPU and memory limits per pod. | `cpu: 100m` |
| `resources.requests` | CPU and memory requests per pod. | `memory: 128Mi` |
| `autoscaling.enabled` | Enables horizontal autoscaling. | `false` |
| `autoscaling.minReplicas` | Minimum number of replicas. | `1` |
| `autoscaling.maxReplicas` | Maximum number of replicas. | `100` |
| `autoscaling.targetCPUUtilizationPercentage` | CPU utilization target for the HPA. | `80` |
| `volumes` | Additional volumes for deployments. | `secret` |
| `volumeMounts` | Additional volume mounts. | `/etc/foo` |
| `nodeSelector` | Node selection for pods. | `{}` |
| `tolerations` | Tolerations for tainted nodes. | `[]` |
| `affinity` | Affinity and anti-affinity rules. | `{}` |


