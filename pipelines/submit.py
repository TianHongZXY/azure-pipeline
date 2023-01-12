import os
import sys
from dataclasses import dataclass
from pathlib import Path

from azureml.core import Workspace
from azureml.core import Dataset, Datastore
from azure.ml.component import (
    Component,
    dsl,
)
import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import to_absolute_path
from azureml.core.authentication import InteractiveLoginAuthentication
from azure.ai.ml import Input


@dataclass
class AMLConfigIP:
    workspace_name: str
    resource_group: str
    subscription_id: str
    cpu_target: str
    experiment_name: str


@dataclass
class TrainerArgs:
    benchmark_name: str


@dataclass
class DataConfigs:
    train_file: str
    # dev_file: str
    # test_file: str


@dataclass
class PipelineConfig:
    data_configs: DataConfigs
    trainer: TrainerArgs
    aml: AMLConfigIP


cs = ConfigStore.instance()
cs.store(name="config", node=PipelineConfig)


@hydra.main(config_path="configs", config_name=f"test_pipeline.yaml")
def main(config: PipelineConfig):
    # connect to your Azure ML workspace
    ws = Workspace(
        subscription_id=config.aml.subscription_id,
        resource_group=config.aml.resource_group,
        workspace_name=config.aml.workspace_name,
    )
    def_blob_store = Datastore(ws, "workspaceblobstore")

    data_file = Dataset.File.from_files([(def_blob_store, 'hotpotqa/')])
    # train_data = ws.datasets[config.data_configs.train_file]
    # dev_data = ws.datasets[config.data_configs.dev_file]
    # test_data = ws.datasets[config.data_configs.test_file]

    file_path = Path(to_absolute_path(__file__))
    root_directory = file_path.parent.parent.absolute()

    load_data_func = Component.from_yaml(ws, yaml_file=os.path.join(root_directory, "components", "load_data", "load_data.yaml"))

    # data_file = f"azureml://subscriptions/{ws.subscription_id}/resourcegroups/{ws.resource_group}/workspaces/{config.aml.workspace_name}/datastores/workspaceblobstore/paths/hotpotqa"
    @dsl.pipeline(
        name=config.trainer.benchmark_name,
        display_name=config.trainer.benchmark_name,
        description=config.trainer.benchmark_name,
        default_compute_target="v-xinyuzhu1", #config.aml.cpu_target,
    )
    def test_pipeline():
        outputs = load_data_func(data_dir=data_file)
        # outputs.runsettings.target = "cpu_cluster"

    pipeline = test_pipeline()
    _ = pipeline.submit(experiment_name=config.aml.experiment_name)

if __name__ == "__main__":
    InteractiveLoginAuthentication(tenant_id="bb6afa85-99dc-4914-add4-c9c283c6e87a")# , force=True)
    main()
    print("success")
