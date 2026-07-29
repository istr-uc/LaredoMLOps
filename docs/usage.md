# Usage

Laredo follows a simple workflow: prepare the infrastructure, deploy the platform, and operate the models from the web interface or backend.

## Basic flow

1. Verify that the cluster and dependent services are available.
2. Review the `values.yaml` file and create a new one adjusting the parameters as needed.
3. Install or upgrade the Helm chart.
4. Open the web interface and confirm that the services respond correctly.
5. Create, version, and deploy models according to the project type.

## Typical work cycle

### 1. Prepare a project

Identify the problem type, prepare the dataset csv file and select a name for the proyect.

### 2. Train or register the model

Start the model creation and training process:
1. Select creation mode (Basic or Advanced) and problem type
2. Upload data, confirm data types and target variable
3. Select the preprocessing algorithms
4. Select the ML algorithm and configure the parameters.
5. Inspect model details and evaluation results.

For a practical example, see the detailed guides:
- [Basic creation mode](basic-creation-mode.md) for a guided workflow.
- [Advanced creation mode](advanced-creation-mode.md) for a more configurable pipeline.

### 3. Deploy

Once the model has been validated, deploy the specific version you want to expose.

### 4. Check deployment

After deploying the model you can access to the Swagger docs to check the endpoints and perform a health check.