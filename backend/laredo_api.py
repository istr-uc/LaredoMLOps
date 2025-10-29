import os
from creation_types import *
from preprocessing_strategy import *
from model_strategies import *
import pandas as pd
from flask import Flask, jsonify, request, request
from flask_restful import Api
from flask_cors import CORS
import pandas as pd
import jinja2
from kubernetes import client, config
import yaml
from utils import ValidationError



app = Flask(__name__)
CORS(app)
api = Api(app=app)

ip = os.environ['TRACKING_URI_IP']
port = os.environ['TRACKING_URI_PORT']
mlflow.set_tracking_uri(f"http://{ip}:{port}")
# mlflow.set_tracking_uri(f"http://localhost:5000") # For local testing

CREATION_TYPE = {
    "BASIC": ModelBasicCreation,
    "ADVANCED": ModelAdvancedCreation
}

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

    is_deployed =  search_deployment(model_name)

    response_data = {
        "estimator": estimator,
        "metrics" : run.data.metrics,
        "dataset" : dataset,
        "is_deployed" : is_deployed
    }

    return jsonify(response_data), 200

@app.route('/models', methods=['POST'])
def train_model():
    data = request.json

    type_str : str = data.get('creationType')
    params = data.get("params", {})
    model_creation_type = CREATION_TYPE.get(type_str.upper())
    
    if model_creation_type is None:
        return jsonify({
            "error": f"Invalid creation type '{type_str}'. Must be one of: {list(CREATION_TYPE.keys())}" 
        }), 400

    model_creator = model_creation_type(**params)
    metrics = model_creator.create()

    return jsonify(metrics), 201


@app.route("/models/<model_name>/deploy", methods=["POST"])
def model_deploy(model_name):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "languageWrapper_template.jinja"
    template = templateEnv.get_template(TEMPLATE_FILE)

    data = {
        "deployment_name": model_name,
        "model_name": model_name,
        "replicas": 1,
        "tracking_uri_ip": ip,
        "tracking_uri_port": port,
        "is_k8s": True
    }

    outputText = template.render(data)
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

    deployments = v1.list_namespaced_custom_object(
        group="machinelearning.seldon.io",
        version="v1",
        plural="seldondeployments",
        namespace="laredo")


    deployments = deployments["items"]
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


@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    response = jsonify({"error": e.message})
    response.status_code = e.status_code
    return response

if __name__ == "__main__":
    app.run(port=5050, debug=True)