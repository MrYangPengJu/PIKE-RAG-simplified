# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import argparse
import importlib
import os
import pathlib
import shutil
import warnings
import yaml

# TODO
warnings.filterwarnings("ignore", r".*TypedStorage is deprecated.*")
warnings.filterwarnings("ignore", r".*Relevance scores must be between 0 and 1.*")
warnings.filterwarnings("ignore", r".*No relevant docs were retrieved using the relevance score threshold 0.5.*")

from pikerag.utils.config_loader import load_dot_env
from pikerag.workflows.qa import QaWorkflow


def load_yaml_config(config_path: str, args: argparse.Namespace) -> dict:
    # YAML 文件的语法严格区分缩进，并且 缩进必须使用空格，不能使用 Tab 键。
    with open(config_path, "r", encoding='utf-8') as fin:
        yaml_config: dict = yaml.safe_load(fin)

    # Create logging dir if not exists
    experiment_name = yaml_config["experiment_name"]
    log_dir = os.path.join(yaml_config["log_root_dir"], experiment_name)
    yaml_config["log_dir"] = log_dir
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    shutil.copy(config_path, log_dir)

    # test jsonl file path
    if yaml_config["test_jsonl_filename"] is None:
        yaml_config["test_jsonl_filename"] = f"{experiment_name}.jsonl"
    yaml_config["test_jsonl_path"] = os.path.join(log_dir, yaml_config["test_jsonl_filename"])

    # LLM cache config
    if yaml_config["llm_client"]["cache_config"]["location_prefix"] is None:
        yaml_config["llm_client"]["cache_config"]["location_prefix"] = experiment_name

    return yaml_config


if __name__ == "__main__":
    # 加载配置文件
    fixed_config_path = "QA.yml"
    yaml_config: dict = load_yaml_config(fixed_config_path, None)


    # Load environment variables from dot env file.
    # 如果使用的是本地模型（比如 LocalDeepSeekClient），并不依赖 OpenAI/Azure Key，那可以 不设置 dotenv_path
    # load_dot_env(env_path=yaml_config.get("dotenv_path", None))

    # Dynamically import the QA Workflow class
    workflow_module = importlib.import_module(yaml_config["workflow"]["module_path"])
    workflow_class = getattr(workflow_module, yaml_config["workflow"]["class_name"])
    assert issubclass(workflow_class, QaWorkflow)
    workflow = workflow_class(yaml_config)

    workflow.run()
