import asyncio
import os
import time

import boto3
import mlflow
import pandas as pd
from flask import Flask, jsonify, request, request
from flask_restful import Api
from flask_cors import CORS
import jinja2
from kubernetes import client, config
import yaml
import json



app = Flask(__name__)
CORS(app)
api = Api(app=app)

ip = os.environ['TRACKING_URI_IP']
port = os.environ['TRACKING_URI_PORT']
mlflow.set_tracking_uri(f"http://{ip}:{port}")
# mlflow.set_tracking_uri(f"http://localhost:5000") # For local testing


config.load_incluster_config()
configuration = client.Configuration.get_default_copy()
api_client = client.ApiClient(configuration)
batch_v1 = client.BatchV1Api(api_client)


@app.route("/")
def hello():
    return "Esta es mi API creada para usar los datos de MlFlow en React"

@app.route("/models", methods=["GET"])
def get_models():
    registered_models = mlflow.search_registered_models()

    if not registered_models:
        return jsonify({"error": "No models found"}), 404

    filtered_models = [{
        'version': model.latest_versions[0].version,
        'model_name': model.latest_versions[0].name,
        'creation_time': model.latest_versions[0].creation_timestamp,
        'is_deployed' : search_deployment(model.latest_versions[0].name)
    } for model in registered_models]

    sorted_models = sorted(filtered_models, key=lambda x: x['creation_time'], reverse=True)

    return jsonify(sorted_models), 200


@app.route("/models/<model_name>", methods=["GET"])
def get_model(model_name):
    model = mlflow.search_registered_models(filter_string=f"name='{model_name}'")

    if not model:
        return jsonify({"error": "Model not found"}), 404

    run_id = model[0].latest_versions[0].run_id
    run = mlflow.get_run(run_id)
    estimator_uri = run.info.artifact_uri + "/estimator.html"
    estimator = mlflow.artifacts.load_text(estimator_uri)
    dataset = run.inputs.dataset_inputs[0].dataset.schema
    if dataset == '' or dataset is None:
        dataset = '{}'
    try:
        is_deployed =  search_deployment(model_name)
    except:
        is_deployed = False

    response_data = {
        "estimator": estimator,
        "metrics" : run.data.metrics,
        "dataset" : dataset,
        "is_deployed" : is_deployed
    }
    # print("response_data: ", response_data) # Debugging line
    return jsonify(response_data), 200

@app.route('/models', methods=['POST'])
def train_model():

    # Get params form request body
    data = request.json

    type_str : str = data.get('creationType')
    params = data.get("params", {})
    # Get dataset name from params, if not present, return error
    dataset_name = params.pop("datasetFilename")
    params["datasetURL"] = get_s3_signed_url(dataset_name, method="get_object")
    # Create mlflow run and get run id
    with mlflow.start_run() as run:
        run_id = run.info.run_id
    
    # try:
    #     # This look for a kube-config file, which is the default way to connect to a kubernetes cluster, but it won't work if the backend is running inside the cluster, so we need to load the in-cluster configuration if the kube-config file is not found
    #     config.load_kube_config() 
    # except config.config_exception.ConfigException:
    #     try:
    #         # This load the in-cluster configuration, 
    #         # which is the way to connect to the kubernetes cluster 
    #         # when the backend is running inside the cluster
    #         config.load_incluster_config()
    #     except config.config_exception.ConfigException:
    #         return jsonify({"error": "Failed to load both kube-config file and in-cluster configuration."}), 500
    
    container = client.V1Container(
        name="trainer",
        image=os.getenv("TRAINER_IMAGE") + ":" + os.getenv("TRAINER_TAG"),
        env=[
            client.V1EnvVar(
                name="PARAMS",
                value=json.dumps(params)
            ),
            client.V1EnvVar(
                name="CREATION_TYPE",
                value=type_str
            ),
            client.V1EnvVar(
                name="RUN_ID",
                value=run_id
            ),
            client.V1EnvVar(
                name="TRACKING_URI_IP",
                value=os.getenv("TRACKING_URI_IP")
            ),
            client.V1EnvVar(
                name="TRACKING_URI_PORT",
                value=os.getenv("TRACKING_URI_PORT")
            )
        ]
    )
    template = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(
            restart_policy="Never",
            containers=[container]
        )
    )

    job_spec = client.V1JobSpec(template=template)

    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name="trainer-job-" + run_id),
        spec=job_spec
    )

    namespaced_job =batch_v1.create_namespaced_job("laredo", job)
    
    # return jsonify(run_id), 201
    return jsonify({
        "job_id": job.metadata.name,
        "run_id": run_id,
        "status": "running"
    }), 201

@app.route("/job/status", methods=["GET"])
# def get_job_status(job_id):
def get_job_status():
    job_id = request.args.get("jobId")
    run_id = request.args.get("runId")
    # job = client.BatchV1Api().read_namespaced_job_status(
    job = batch_v1.read_namespaced_job_status(
        name=job_id,
        namespace="laredo"
    )

    if job.status.succeeded:
        # return "succeeded"
        return jsonify({"status": "succeeded", "results": get_run_metrics(run_id)})
    if job.status.failed:
        # return "failed"
        return jsonify({"status": "failed"})
    # return "running"
    return jsonify({"status": "running"})


def get_run_metrics(run_id):
    run = mlflow.get_run(run_id)
    return run.data.metrics

def get_s3_signed_url(dataset_name,method="get_object"):
    s3_client = boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    bucket_name = os.getenv("DATASET_BUCKET_NAME")
    signed_url = s3_client.generate_presigned_url(
        method,
        Params={'Bucket': bucket_name, 'Key': dataset_name},
        ExpiresIn=3600  # URL expires in 1 hour
    )
    return signed_url

@app.route("/models/<run_id>/status", methods=["GET"])
def get_model_status(run_id):
    run = mlflow.get_run(run_id)
    return jsonify({
        "status": run.info.status,
        "run_id": run_id
    }), 200

def render_template(template_name, data):
    templateLoader = jinja2.FileSystemLoader(searchpath="src/resources/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(template_name)
    outputText = template.render(data)
    return outputText

@app.route("/models/<model_name>/deploy", methods=["POST"])
def model_deploy(model_name):
    # templateLoader = jinja2.FileSystemLoader(searchpath="./")
    # templateLoader = jinja2.FileSystemLoader(searchpath="src/resources/")
    # templateEnv = jinja2.Environment(loader=templateLoader)
    # TEMPLATE_FILE = "languageWrapper_template.jinja"
    # template = templateEnv.get_template(TEMPLATE_FILE)

    data = {
        "deployment_name": model_name,
        "model_name": model_name,
        "replicas": 1,
        "tracking_uri_ip": ip,
        "tracking_uri_port": port,
        "is_k8s": True
    }

    # outputText = template.render(data)
    outputText = render_template("languageWrapper_template.jinja", data)
    dep = yaml.safe_load(outputText)

    # config.load_kube_config()

    try:
        config.load_kube_config()
    except config.config_exception.ConfigException:
        # `load_kube_config` assumes a local kube-config file, and fails if not
        # present, raising:
        #
        #     kubernetes.config.config_exception.ConfigException: Invalid
        #     kube-config file. No configuration found.
        #
        # Since running a parsl driver script on a kubernetes cluster is a common
        # pattern to enable worker-interchange communication, this enables an
        # in-cluster config to be loaded if a kube-config file isn't found.
        #
        # Based on: https://github.com/kubernetes-client/python/issues/1005
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException:
            return jsonify({"error": "Failed to load both kube-config file and in-cluster configuration."}), 500


    v1 = client.CustomObjectsApi()

    resp = v1.create_namespaced_custom_object(
        group="machinelearning.seldon.io",
        version="v1",
        plural="seldondeployments",
        body=dep,
        namespace="laredo")

    return jsonify(), 201

@app.route("/models/<model_name>/deploy", methods=["DELETE"])
def delete_deployment(model_name):
    '''
    Delete a deployment with the given model name
    Args:
        model_name: str
    '''
    try:
        config.load_kube_config()
    except config.config_exception.ConfigException:
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException:
            return jsonify({"error": "Failed to load both kube-config file and in-cluster configuration."}), 500

    v1 = client.CustomObjectsApi()

    resp = v1.delete_namespaced_custom_object(
        group="machinelearning.seldon.io",
        version="v1",
        plural="seldondeployments",
        name=f"laredo-server-{model_name}", 
        namespace="laredo")

    return jsonify(), 204


def get_deployments():
    '''
    Get all the deployments in the laredo namespace
    Returns:
        List of deployments
    '''
    try:
        config.load_kube_config()
    except config.config_exception.ConfigException:
        try:
            config.load_incluster_config()
        except config.config_exception.ConfigException:
            raise config.config_exception.ConfigException(
                "Failed to load both kube-config file and in-cluster configuration."
            )

    v1 = client.CustomObjectsApi()

    # If not found, raises catch the exception and return an empty list
    try:
        deployments = v1.list_namespaced_custom_object(
            group="machinelearning.seldon.io",
            version="v1",
            plural="seldondeployments",
            namespace="laredo")
        deployments = deployments["items"]
    except client.exceptions.ApiException as e:
        deployments = []

    #print("deployments: ", len(deployments))
    return deployments


def search_deployment(model_name):
    '''
    Search for a deployment with the given model name
    Args:
        model_name: str
    Returns:
        True if the deployment exists, False otherwise
    '''
    deployments = get_deployments()


    for deployment in deployments:
        if deployment["metadata"]["name"] == f"laredo-server-{model_name}":
            return True


    return False

@app.route("/column-types" , methods=["POST"])
def get_column_types():
    data = request.json

    dataset_json = data.get('datasetJSON')

    if not dataset_json:
        return jsonify({"message": "Missing dataset"}), 400
    
    dataset = pd.DataFrame.from_dict(dataset_json)

    column_types = dataset.dtypes.apply(lambda x: x.name).to_dict()
    
    return jsonify(column_types), 200

@app.route("/obtain-s3-presigned-put-url", methods=["POST"])
def get_s3_signed_put_url():
    data = request.json
    dataset_filename = data.get('datasetFilename')
    presigned_url = get_s3_signed_url(dataset_name=dataset_filename, method="put_object")
    
    print(f"Generated presigned URL for {dataset_filename}: {presigned_url}") # Debugging line
    return jsonify({"presigned_url": presigned_url}), 200

class ValidationError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    response = jsonify({"error": e.message})
    response.status_code = e.status_code
    return response

if __name__ == "__main__":
    app.run(port=5050, debug=True)
