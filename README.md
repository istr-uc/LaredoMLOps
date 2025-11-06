# Laredo: Democratizing ML lifecicle management 

## What is Laredo?

Laredo is a software tool that simplifies the process of creating, versioning, deploying and monitoring scalable machine learning pipelines based on scikit-learn, autogluon, pytorch (soon) and keras (soon).

Laredo is built on top of well known and reliable technologies:
- **Kubernetes** to handle the virtualization, horizontal scaling and routing of the machine learning pipelines.
- **MLFlow** as a model repository where the metadata and binaries of the models are stores to allow easy vesion control.
- **Seldon Core** to wrap the models as gRPC or REST services and deploy them automatically.
- **Helm** to pack all the diferent components that comprise the tool simplify the deployment and reconfiguration.
- **Scikit-learn** to implement the machine learning algorithms and preprocessing pipelines
- **Autogluon** auto-ml framework to train the models in the easy mode section of the tool.

## Requirements

In order to succesfully deploy and use Laredo you should have:
- A running kubernetes cluster
- [Seldon Core](https://docs.seldon.io/projects/seldon-core/en/latest/nav/installation.html) up and running on the kubernetes cluster
- [MlFlow](https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html) server to connect Laredo.
- A helm client available.

## Install and start Laredo

Laredo ships as a Helm chart that automatically deploys the backend and frontend containers on a prexisting Kubernetes cluster (see Requierements).

To run Laredo the only thing needed is to ensure you meet all the requirements, fill the values.yaml and run the command:

```helm install laredo -f values```

After a few seconds you can access the Laredo web UI using.

> [!NOTE]
> The first time executing the command or after an update it migth take longer because it need to download the containers from the registry.

A more detailed description of the intallation process, including the installation of the prerequired components it available at [Instalation guide](tutotials/Installation_guide.md)

### Required values.yaml parameters

| Name       | Type       | Description |
|------------|------------|-------------|
| mlflow_uri   | str     |  URI of the MlFlow server|
| mlflow_port   | str     | Port of the MlFlow server |

## Credits
This is the main Laredo repository and integrates all the previous developments. From now on, evolution and maintenance of Laredo will be managed and performed here.
- Original UI repository: [Laredo User Interface](https://github.com/iBerrouet/TFGLaredo)
- Original LaredocMind repository: [LaredocMind](https://github.com/Gabiz053/LaredocMind)

By University of Cantabria.
@author Isaac Berrouet Santos
@author Gabriel Gómez García
@author Ricardo Dintén
@supervisor Marta Zorrilla