import argparse
import os
from typing import Any, Dict, Optional

from fastapi.middleware.cors import CORSMiddleware

import kserve
import mlflow
import pandas as pd
from kserve import Model, ModelServer, logging
from kserve.model_server import app


class LaredoMLModel(Model):
    def __init__(self, name: str):
        super().__init__(name, return_response_headers=True)
        self.name = name
        self.model = None
        self.tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
        self.model_uri = os.getenv("MODEL_URI")
        self._validate_environment()
        self.ready = False
        self.load()

    def _validate_environment(self):
        if not self.tracking_uri:
            raise ValueError("Environment variable MLFLOW_TRACKING_URI is required")
        if not self.model_uri:
            raise ValueError("Environment variable MODEL_URI is required")

    def load(self):
        mlflow.set_tracking_uri(self.tracking_uri)
        self.model = mlflow.pyfunc.load_model(self.model_uri)
        self.ready = True

    def _build_input_dataframe(self, payload: Dict) -> pd.DataFrame:
        if "instances" in payload:
            instances = payload["instances"]
            if isinstance(instances, dict):
                return pd.DataFrame([instances])
            return pd.DataFrame(instances)

        if "inputs" in payload:
            inputs = payload["inputs"]
            if isinstance(inputs, dict):
                return pd.DataFrame([inputs])
            return pd.DataFrame(inputs)

        if isinstance(payload, dict) and payload:
            return pd.DataFrame([payload])

        raise ValueError("Request payload must contain 'instances' or 'inputs' with valid data")

    async def predict(
        self,
        payload: Dict,
        headers: Optional[Dict[str, str]] = None,
        response_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        input_df = self._build_input_dataframe(payload)
        predictions = self.model.predict(input_df)

        if isinstance(predictions, pd.DataFrame):
            predictions = predictions.to_dict(orient="records")
        elif isinstance(predictions, pd.Series):
            predictions = predictions.tolist()
        elif hasattr(predictions, "tolist"):
            try:
                predictions = predictions.tolist()
            except Exception:
                predictions = [predictions]

        return {"predictions": predictions}


parser = argparse.ArgumentParser(parents=[kserve.model_server.parser])
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    if args.configure_logging:
        logging.configure_logging(args.log_config_file)

    model = LaredoMLModel(name=os.getenv("MODEL_NAME", "laredo-mlflow-model"))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ModelServer().start([model])