import os
import sys
from dataclasses import dataclass
from pathlib import Path

from azureml.core import Workspace
from azure.ml.component import (
    Component,
    dsl,
)
import hydra
from hydra.core.config_store import ConfigStore
from hydra.utils import to_absolute_path


# @dataclass
# class AMLConfigIP:
#     workspace_name: str
#     resource_group: str
#     subscription_id: str
#     cpu_target: str
#     gpu_target: str
#     gpu_target_openai: str
#     experiment_name: str
#     gpt3_model_selector: str
#     gpt3_onebox_inference: str


@dataclass
class TrainerArgs:
    benchmark_name: str


# @dataclass
# class DataConfigs:
#     train_file: str
#     dev_file: str
#     test_file: str


@dataclass
class PipelineConfig:
    # data_configs: DataConfigs
    trainer: TrainerArgs
    # aml: AMLConfigIP


cs = ConfigStore.instance()
cs.store(name="config", node=PipelineConfig)


@hydra.main(config_path="configs", config_name=f"test_pipeline.yaml")
def main(config: PipelineConfig):
    # connect to your Azure ML workspace
    ws = Workspace(
        subscription_id="521f9448-5428-4a47-b228-f34801eaaa26", # config.aml.subscription_id,
        resource_group="aicode", # config.aml.resource_group,
        workspace_name="aicode", # config.aml.workspace_name,
    )

    # train_data = ws.datasets[config.data_configs.train_file]
    # dev_data = ws.datasets[config.data_configs.dev_file]
    # test_data = ws.datasets[config.data_configs.test_file]

    file_path = Path(to_absolute_path(__file__))
    root_directory = file_path.parent.parent.absolute()

    load_data_func = Component.from_yaml(ws, yaml_file=os.path.join(root_directory, "components", "load_data", "load_data.yaml"))

    data_file = f"azureml://subscriptions/ws.subscription_id/resourcegroups/ws.resource_group/workspaces/ws.workspace_name/datastores/workspaceblobstore/paths/hotpotqa/hotpot_dev_v1_simplified.json"
    data = load_data_func(data_file)
    print(data[0])

