import os
import json

from flask import jsonify

from src.utils.creation_types import *
from src.utils.model_strategies import *
from src.utils.preprocessing_strategy import *

CREATION_TYPE = {
    "BASIC": ModelBasicCreation,
    "ADVANCED": ModelAdvancedCreation
}

def train_model(run_id: str, type_str: str, params: dict):
    model_creation_type = CREATION_TYPE.get(type_str.upper())
    if model_creation_type is None:
        # Set run status to failed in mlflow
        mlflow.set_tag("mlflow.runStatus", "FAILED")
        return jsonify({
            "error": f"Invalid creation type '{type_str}'. Must be one of: {list(CREATION_TYPE.keys())}" 
        }), 400
    print(f"Received request to create model with type '{type_str}' and params: {params}") # Debugging line
    model_creator = model_creation_type(run_id=run_id, **params)
    model_creator.create()

    # return jsonify(metrics), 201


def main():
    # Set mlflow tracking uri from environment variables
    ip = os.environ['TRACKING_URI_IP']
    port = os.environ['TRACKING_URI_PORT']
    mlflow.set_tracking_uri(f"http://{ip}:{port}")
    # Read params from environment variables
    run_id = os.environ.get("RUN_ID")
    type_str = os.environ.get("CREATION_TYPE")
    params_str = os.environ.get("PARAMS", "{}")
    # Convert params from json to dict
    params = json.loads(params_str)
    train_model(run_id, type_str, params)
    pass

if __name__ == "__main__":
    main()