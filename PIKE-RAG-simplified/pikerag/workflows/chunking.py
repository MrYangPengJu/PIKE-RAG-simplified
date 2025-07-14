# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import importlib
import os
from typing import List, Tuple

import pickle
from tqdm import tqdm

from pikerag.document_loaders import get_loader
from pikerag.document_transformers import LLMPoweredRecursiveSplitter
from pikerag.llm_client import BaseLLMClient
from pikerag.utils.config_loader import load_class
from pikerag.utils.logger import Logger
from pikerag.utils.walker import list_files_recursively


class ChunkingWorkflow:
    def __init__(self, yaml_config: dict) -> None:
        # 读取配置 yaml_config
        # 初始化日志、模型、切分器、文件路径等
        self._yaml_config: dict = yaml_config

        self._init_logger()
        self._init_splitter()

        self._init_file_infos()
        return

    def _init_logger(self) -> None:
        # 创建一个自定义 Logger 实例，输出日志到指定目录。
        self._logger: Logger = Logger(
            name=self._yaml_config["experiment_name"],
            dump_folder=self._yaml_config["log_dir"],
        )

    def _init_llm_client(self) -> None:
        # Dynamically import the LLM client.
        # 动态导入本地或远程大语言模型（LLM）客户端类（如 LocalDeepSeekClient），并初始化。支持缓存策略，避免重复调用模型。
        self._client_logger = Logger(name="client", dump_mode="a", dump_folder=self._yaml_config["log_dir"])

        llm_client_config = self._yaml_config["llm_client"]
        cache_location = os.path.join(
            self._yaml_config["log_dir"],
            f"{llm_client_config['cache_config']['location_prefix']}.db",
        )

        client_module = importlib.import_module(llm_client_config["module_path"])
        client_class = getattr(client_module, llm_client_config["class_name"])
        assert issubclass(client_class, BaseLLMClient)
        self._client = client_class(
            location=cache_location,
            auto_dump=llm_client_config["cache_config"]["auto_dump"],
            logger=self._client_logger,
            llm_config=llm_client_config["llm_config"],
            **llm_client_config.get("args", {}),
        )
        return

    def _init_splitter(self) -> None:
        # 动态加载一个“切分器”类（可能是基于 LLM 的）
        # 如果该切分器需要 LLM，则提前初始化 LLM
        # 设置协议函数用于摘要、重新切分、文本结构识别
        splitter_config: dict = self._yaml_config["splitter"]
        splitter_args: dict = splitter_config.get("args", {})

        splitter_class = load_class(
            module_path=splitter_config["module_path"],
            class_name=splitter_config["class_name"],
            base_class=None,
        )

        if issubclass(splitter_class, (LLMPoweredRecursiveSplitter)):
            # Initialize LLM client
            self._init_llm_client()

            # Update args
            splitter_args["llm_client"] = self._client
            splitter_args["llm_config"] = self._yaml_config["llm_client"]["llm_config"]

            splitter_args["logger"] = self._logger

        if issubclass(splitter_class, LLMPoweredRecursiveSplitter):
            # 判断当前加载的切块类（splitter_class）是否是 LLMPoweredRecursiveSplitter 的子类。这个类是 PIKE-RAG 中专为依赖 LLM 的切块流程设计的。
            # Load protocols
            protocol_configs = self._yaml_config["chunking_protocol"]
            # 从配置文件 chunking.yml 中读取 "chunking_protocol" 字段，得到一个包含多个协议配置项的字典,例如
            '''
            chunking_protocol:
                module_path: pikerag.prompts.chunking.protocols
                chunk_summary: chunk_summary_protocol
                chunk_summary_refinement: chunk_summary_refinement_protocol
                chunk_resplit: chunk_resplit_protocol
            '''
            # 动态导入 chunking.yml 中指定的协议模块，这意味着这些“协议”函数是在这个模块里定义的
            protocol_module = importlib.import_module(protocol_configs["module_path"])
            # 从模块中获取用于 初始摘要生成 的函数（或类、协议对象），用于 first_chunk_summary_protocol 参数
            chunk_summary_protocol = getattr(protocol_module, protocol_configs["chunk_summary"])
            # 获取用于 后续摘要细化（refinement） 的协议函数。用于处理“最后一个 chunk”的摘要
            chunk_summary_refinement_protocol = getattr(protocol_module, protocol_configs["chunk_summary_refinement"])
            # 获取用于 重新切块（resplit）的协议函数。如果 chunk 粒度不合适，比如太大或太小，就会用这个协议来重新切一遍。
            chunk_resplit_protocol = getattr(protocol_module, protocol_configs["chunk_resplit"])

            # Update args
            # 把以上 3 个协议注入到 splitter_args 中，作为初始化 LLMPoweredRecursiveSplitter 所需的参数。
            splitter_args["first_chunk_summary_protocol"] = chunk_summary_protocol
            splitter_args["last_chunk_summary_protocol"] = chunk_summary_refinement_protocol
            splitter_args["chunk_resplit_protocol"] = chunk_resplit_protocol
        # 如果把 LLMPoweredRecursiveSplitter 比作一个厨师，这段代码就相当于“告诉厨师你要的切菜顺序、切法、最后装盘方式”，而这些规则写在 chunking.yml 菜谱里，代码会自动读菜谱，分配好工具和步骤
        self._splitter = splitter_class(**splitter_args)
        return

    def _init_file_infos(self) -> None:
        # 获取待处理文档路径、扩展名
        # 为每个文档构建输出文件名（如 .pkl）
        input_setting: dict = self._yaml_config.get("input_doc_setting")
        output_setting: dict = self._yaml_config.get("output_doc_setting")
        assert input_setting is not None and output_setting is not None, (
            f"input_doc_setting and output_doc_setting should be provided!"
        )

        input_file_infos = list_files_recursively(
            directory=input_setting.get("doc_dir"),
            extensions=input_setting.get("extensions"),
        )

        output_dir = output_setting.get("doc_dir")
        output_suffix = output_setting.get("suffix", "pkl")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        self._file_infos: List[Tuple[str, str, str]] = [
            (doc_name, doc_path, os.path.join(output_dir, f"{os.path.splitext(doc_name)[0]}.{output_suffix}"))
            for doc_name, doc_path in input_file_infos
        ]
        return

    def run(self) -> None:
        # 对每个文档进行加载、切分、处理、添加元信息
        # 最后把结果保存到 .pkl 文件中，供后续 RAG 检索使用
        for doc_name, input_path, output_path in tqdm(self._file_infos, desc="Chunking file"):
            if os.path.exists(output_path) is True:
                self._logger.info(f"Skip file: {doc_name} due to output already exist!")
                continue

            self._logger.info(f"Loading file: {doc_name}")

            # Try get the file loader and load documents
            doc_loader = get_loader(file_path=input_path, file_type=None)
            if doc_loader is None:
                self._logger.info(f"Skip file {doc_name} due to undefined Document Loader.")
                continue
            docs = doc_loader.load()

            # Add metadata
            # for doc in docs:
            #     doc.metadata.update({"filename": doc_name})
            for index, doc in enumerate(docs, start=1):
                doc.metadata.update({"filename":doc_name})
                doc.metadata.update({"chunk_id":str(index)})

            # Document Splitting
            chunk_docs = self._splitter.transform_documents(docs)

            # Dump document chunks to disk.
            with open(output_path, "wb") as fout:
                pickle.dump(chunk_docs, fout)
