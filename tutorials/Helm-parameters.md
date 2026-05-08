# LaredoMLOps Helm Chart Configuration Guide

This guide provides an overview of the configurable parameters in the `values.yaml` file for the LaredoMLOps Helm chart.

## 🚀 Core Configuration (Mandatory for Custom Deployments)
These parameters are essential to ensure the correct images are pulled and the services are reachable within the cluster.

| Parameter | Description |
| :------ | :--- |
| `backend.image.repository` | The Docker repository for the Backend API image. |
| `backend.image.tag` | The specific version/tag of the Backend API image to deploy. |
| `frontend.image.repository` | The Docker repository for the Frontend UI image. |
| `frontend.image.tag` | The specific version/tag of the Frontend UI image to deploy. |
| `chatbotBackend.image.repository` | The Docker repository for the Chatbot Backend image. |
| `chatbotBackend.image.tag` | The specific version/tag of the Chatbot Backend image to deploy. |
| `backend.service.port` | The port on which the Backend API service is exposed. |
| `frontend.service.port` | The port on which the Frontend UI service is exposed. |
| `chatbotBackend.service.port` | The port on which the Chatbot Backend service is exposed. |

---

## 🛠️ Infrastructure Toggles (Critical for Feature Set)
Use these to decide which supporting services (Postgres, S3, MLflow) are deployed along with the main application.

| Parameter | Description |
| :------ | :--- |
| `backend.deploy_s3_storage` | Set to `true` to deploy a LocalStack S3 compatible service. |
| `backend.deploy_postgres` | Set to `true` to deploy a PostgreSQL instance. |
| `backend.deploy_mlflow` | Set to `true` to deploy MLflow for model tracking. |

---

## 🛠️ Infrastructure & Service Endpoints (Critical for Connectivity)
These parameters define how the backend interacts with the deployed or external services.

### 📦 S3 / LocalStack Configuration
| Parameter | Description |
| :------ | :--- |
| `backend.s3_storage_size` | Size of the S3 storage volume. |
| `backend.s3_service_port` | Port for the S3 service. |
| `backend.S3_INTERNAL_ENDPOINT_URL` | Internal cluster URL for S3. |
| `backend.MLFLOW_S3_ENDPOINT_URL` | External URL for S3 access. |
| `backend.AWS_ACCESS_KEY_ID` | AWS access key for S3 authentication. |
| `backend.AWS_SECRET_ACCESS_KEY` | AWS secret key for S3 authentication. |
| `backend.AWS_DEFAULT_REGION` | The AWS region to use. |
| `backend.DATASET_BUCKET_NAME` | Name of the bucket for datasets. |

### 🐘 PostgreSQL Configuration
| Parameter | Description |
| :------ | :--- |
| `backend.postgres_service_port` | Port for the PostgreSQL service. |
| `backened.postgres_admin_password` | Password for the admin user. |
| `backend.postgres_db_name` | Name of the database to create. |
| `backend.postgres_user` | Username for database access. |
| `backend.postgres_password` | Password for database access. |
| `backend.postgres_host` | Hostname/Service name of the Postgres instance. |

### 🧪 MLflow Configuration
| Parameter | Description |
| :------ | :--- |
| `backend.mlflow_tracking_uri_ip` | Service name/IP for the MLflow tracking server. |
| `backend.mlflow_tracking_uri_port` | Port for the MLflow tracking server. |
| `backend.mlflow_externalStorage` | Whether to use external storage for artifacts. |
| `backend.mlflow_artifact_uri` | The S3 URI for storing MLflow artifacts. |

---

## 🌐 Networking & Access (Optional)
Configuration for how the services are accessed from outside the cluster.

### Gateway API (Modern Kubernetes Networking)
*   `gatewayAPI.enabled`: Enable the newer Kubernetes Gateway API configuration.
*   `gatewayAPI.hosts`: Configure HTTPRoutes for `localstack`, `mlflow`, and `frontend` services.
*   `gatewayAPI.corsPolicy`: Define CORS rules (allowed methods, headers, and origins).

---

## 📈 Scaling & Resource Management (Optional)
Use these to optimize performance and resource consumption.

| Parameter | Description |
| :------ | :--- |
| `*.replicaCount` | The number of pod instances to run for each component. |
| `autoscaling.enabled` | Enable Horizontal Pod Autoscaler (HPA). |
| `autoscaling.maxReplicas` | The maximum number of pods the HPA can scale up to. |
| `resources.limits` | Set CPU and Memory limits to prevent a single pod from consuming all node resources. |
| `resources.requests` | Set CPU and Memory requests to ensure the scheduler finds a suitable node. |

---

## 🛡️ Security & Identity (Optional)
Parameters for hardening the deployment.

| Parameter | Description |
| :------ | :--- |
| `*.serviceAccount.create` | Whether to create a dedicated ServiceAccount for the component. |
| `*.podSecurityContext` | Define security settings for the pod (e.g., `fsGroup`). |
| `*.securityContext` | Define security settings for the container (e.g., `runAsUser`, `readOnlyRootFilesystem`). |