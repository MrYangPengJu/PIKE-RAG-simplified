# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import importlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

import jsonlines
from tqdm import tqdm

from pikerag.knowledge_retrievers import BaseQaRetriever
from pikerag.llm_client.base import BaseLLMClient
from pikerag.utils.config_loader import load_class, load_protocol
from pikerag.utils.logger import Logger
from pikerag.workflows.common import BaseQaData, GenerationQaData, MultipleChoiceQaData
from pikerag.workflows.evaluation.evaluator import Evaluator


# TODO: add yaml config checker for it.
class QaWorkflow:
    def __init__(self, yaml_config: dict) -> None:
        self._yaml_config: dict = yaml_config

        self._init_logger()

        self._load_testing_suite()

        self._init_agent()

        self._init_evaluator()

        self._init_qas_metrics_table()

        self._workflow_config: dict = self._yaml_config["workflow"].get("args", {})
        self._num_parallel: int = self._workflow_config.get("num_parallel", 1)

    def _init_logger(self) -> None:
        self._logger: Logger = Logger(
            name=self._yaml_config["experiment_name"],
            dump_folder=self._yaml_config["log_dir"],
        )

    def _load_testing_suite(self) -> None:
        # Dynamically load the test loading function, then load testing suite
        test_loading_module = importlib.import_module(self._yaml_config["test_loading"]["module"])
        test_loading_func = getattr(test_loading_module, self._yaml_config["test_loading"]["name"])
        self._testing_suite: List[BaseQaData] = test_loading_func(**self._yaml_config["test_loading"]["args"])

        assert isinstance(self._testing_suite[0], BaseQaData), f"Loaded test data is not a subclass of BaseQaData."

        self._num_test: int = len(self._testing_suite)
        return

    def _init_protocol(self) -> None:
        # Dynamically import the qa communication protocol
        self._qa_protocol = load_protocol(
            module_path=self._yaml_config["qa_protocol"]["module_path"],
            protocol_name=self._yaml_config["qa_protocol"]["attr_name"],
            partial_values=self._yaml_config["qa_protocol"].get("template_partial", {}),
        )

    def _init_retriever(self) -> None:
        # Dynamically import the chunk retriever
        retriever_config: dict = self._yaml_config["retriever"]

        retriever_class = load_class(
            module_path=retriever_config["module_path"],
            class_name=retriever_config["class_name"],
            base_class=BaseQaRetriever
        )

        self._retriever = retriever_class(
            retriever_config=retriever_config["args"],
            log_dir=self._yaml_config["log_dir"],
            main_logger=self._logger,
        )

    def _init_llm_client(self) -> None:
        # Dynamically import the LLM client. The cache location is left to be set on the start of each round.
        self._client_logger = Logger(name="client", dump_mode="a", dump_folder=self._yaml_config["log_dir"])

        llm_client_config = self._yaml_config["llm_client"]
        client_module = importlib.import_module(llm_client_config["module_path"])
        client_class = getattr(client_module, llm_client_config["class_name"])
        assert issubclass(client_class, BaseLLMClient)

        self.llm_config = llm_client_config["llm_config"]

        self._client = client_class(
            location=None,
            auto_dump=llm_client_config["cache_config"]["auto_dump"],
            logger=self._client_logger,
            llm_config=self.llm_config,
            **llm_client_config.get("args", {}),
        )

    def _update_llm_cache(self, round_idx: int) -> None:
        # Update cache location for different rounds.
        location = os.path.join(
            self._yaml_config["log_dir"],
            f"{self._yaml_config['llm_client']['cache_config']['location_prefix']}_round{round_idx}.db",
        )
        self._client.update_cache_location(location)
        return

    def _init_agent(self) -> None:
        """Initialize the components the `answer` function is going to use. Currently, the `agent` is only a virtual
        concept that there is actually no `agent` instance here (to shorten the instance layers).

        In current implementation, only communication protocol, retriever, LLM client and client logger are initialized
        here to support the 1-step Q&A.
        """
        self._init_protocol()
        self._init_retriever()
        self._init_llm_client()

    def _init_evaluator(self) -> None:
        evaluator_config: dict = self._yaml_config.get("evaluator", {})

        self._evaluator = Evaluator(
            evaluator_config=evaluator_config,
            num_rounds=self._yaml_config["test_rounds"],
            num_data=self._num_test,
            log_dir=self._yaml_config["log_dir"],
            main_logger=self._logger,
        )
        return

    def _init_qas_metrics_table(self) -> None:
        self._qas_logger = Logger("QAS", dump_folder=self._yaml_config["log_dir"], extension_name="csv")

        headers = ["Question", "Label", "Answer"] + [metric.name for metric in self._evaluator._metrics]
        self._qas_logger.debug("|".join(headers))

        return

    def _update_qas_metrics_table(self, qa: BaseQaData) -> None:
        if isinstance(qa, GenerationQaData):
            data = [qa.question, str(qa.answer_labels), str(qa.answer)]
        elif isinstance(qa, MultipleChoiceQaData):
            data = [qa.question, str(qa.answer_mask_labels), str(qa.answer_masks)]
        metrics = [str(qa.answer_metric_scores[metric.name]) for metric in self._evaluator._metrics]

        self._qas_logger.debug("|".join(data + metrics))

        return

    def _update_pbar_desc(self, pbar, round_idx: int, count: int) -> None:
        valid_metrics = []

        em = None
        if "ExactMatch" in self._evaluator._metrics_by_name:
            em = self._evaluator._metrics_by_name["ExactMatch"]._round_total_score / count
            valid_metrics.append(("EM", em))

        f1 = None
        if "F1" in self._evaluator._metrics_by_name:
            f1 = self._evaluator._metrics_by_name["F1"]._round_total_score / count
            valid_metrics.append(("F1", f1))

        accuracy = None
        if "LLM-Accuracy" in self._evaluator._metrics_by_name:
            accuracy = self._evaluator._metrics_by_name["LLM-Accuracy"]._round_total_score / count
            valid_metrics.append(("LLM-Accuracy", accuracy))

        desc_prefix = f"[{self._yaml_config['experiment_name']}] Round {round_idx}"
        if len(valid_metrics) == 0:
            desc = desc_prefix
        else:
            valid_metrics_str = ", ".join([f"{name}: {value:.2%}" for name, value in valid_metrics])
            desc = f"{desc_prefix} ({valid_metrics_str})"

        pbar.set_description_str(desc=desc, refresh=True)
        return

    def _single_thread_run(self) -> None:
        # Create the file handler for the output jsonlines recordings.
        # 从 YAML 配置中读取 test_jsonl_path 字段，创建一个 .jsonl 文件的写入句柄 fout，用于记录每个问题的输出结果
        fout = jsonlines.open(self._yaml_config["test_jsonl_path"], "w")
        # 从配置文件中读取测试轮数（如跑 3 轮，每轮测 100 个问题），外层大循环表示“多轮评估”
        for round_idx in range(self._yaml_config["test_rounds"]):
            round_id: str = f"Round{round_idx}"
            self._update_llm_cache(round_idx)
            self._evaluator.on_round_test_start(round_id)

            question_idx: int = 0
            # self._testing_suite 是所有要测试的问题列表（例如 100 个问答样本）。
            # 用 tqdm 显示进度条，标明当前轮次
            pbar = tqdm(self._testing_suite, desc=f"[{self._yaml_config['experiment_name']}] Round {round_idx}")
            # qa 是一个 GenerationQaData 对象，包含问题、上下文、参考答案等信息
            for qa in pbar:
                # self.answer()：调用系统的核心回答方法，将问题送入 RAG 系统（或 LLM）进行推理
                # 返回 output_dict，其中至少包含 answer 字段（模型生成的答案），以及可能的其他元信息（如解码长度、生成时间等）。
                output_dict: dict = self.answer(qa, question_idx)
                assert "answer" in output_dict, "`answer` should be included in output_dict"
                # 提取出模型答案并填入 qa 对象（即当前问题的结果对象）中
                answer = output_dict.pop("answer")
                qa.update_answer(answer)
                # 其他的元信息（如 logprobs、置信度）更新进 qa.answer_metadata
                qa.answer_metadata.update(output_dict)
                # 更新评估指标
                self._evaluator.update_round_metrics(qa)
                # 将这一问答结果写入 .jsonl
                fout.write(qa.as_dict())
                # 更新可视化表格（可能用于前端界面展示或 TensorBoard）
                self._update_qas_metrics_table(qa)
                question_idx += 1
                # 改变 tqdm 显示的文本，如：“Round 0 | Acc: 83.2%”
                self._update_pbar_desc(pbar, round_idx=round_idx, count=question_idx)
            # 通知评估器这一轮结束，汇总当前轮的统计信息。
            self._evaluator.on_round_test_end(round_id)
        # 通知评估器整个评估流程结束
        self._evaluator.on_test_end()

        fout.close()

    def _multiple_threads_run(self) -> None:
        fout = jsonlines.open(self._yaml_config["test_jsonl_path"], "w")

        for round_idx in range(self._yaml_config["test_rounds"]):
            round_id: str = f"Round{round_idx}"
            self._update_llm_cache(round_idx)
            self._evaluator.on_round_test_start(round_id)

            self._logger.info(f"[{self._yaml_config['experiment_name']}] Round {round_idx} with parallel level set to {self._num_parallel}.")

            with ThreadPoolExecutor(max_workers=self._num_parallel) as executor:
                qa_pbar = tqdm(total=len(self._testing_suite), desc=f"[{self._yaml_config['experiment_name']}] Round {round_idx}")

                # Submit all qa to the executor for question answering
                future_to_index = {
                    executor.submit(self.answer, qa, q_idx): q_idx
                    for q_idx, qa in enumerate(self._testing_suite)
                }

                qas_with_answer: List[BaseQaData] = [None] * len(self._testing_suite)
                for future in as_completed(future_to_index):
                    q_idx = future_to_index[future]
                    qa = self._testing_suite[q_idx]
                    try:
                        output_dict = future.result()

                        # Process output dict one by one
                        assert "answer" in output_dict, "`answer` should be included in output_dict"
                        answer = output_dict.pop("answer")
                        qa.update_answer(answer)
                        qa.answer_metadata.update(output_dict)
                    except Exception as e:
                        print(f"Exception answer {q_idx}-th question: {e}")
                    qas_with_answer[q_idx] = qa

                    qa_pbar.update(1)

                qa_pbar.close()

                evaluation_pbar = tqdm(total=len(self._testing_suite), desc=f"[{self._yaml_config['experiment_name']}] Round {round_idx} Evaluation")

                # Submit all qa to the executor for evaluation
                evaluation_future_to_index = {
                    executor.submit(self._evaluator.update_round_metrics, qa): q_idx
                    for q_idx, qa in enumerate(qas_with_answer)
                }
                for future in as_completed(evaluation_future_to_index):
                    q_idx = evaluation_future_to_index[future]
                    try:
                        future.result()
                    except Exception as e:
                        print(f"Exception evaluate {q_idx}-th question answer: {e}")
                    evaluation_pbar.update(1)

                evaluation_pbar.close()

                for qa in qas_with_answer:
                    fout.write(qa.as_dict())
                    self._update_qas_metrics_table(qa)

            self._evaluator.on_round_test_end(round_id)

        self._evaluator.on_test_end()

        fout.close()

    def run(self) -> None:
        """The QA testing flow."""
        if self._num_parallel == 1:
            return self._single_thread_run()
        else:
            return self._multiple_threads_run()

    def answer(self, qa: BaseQaData, question_idx: int) -> dict:
        """The decision making process when a Question is given.

        Here we implement the process of single LLM call w/ or w/o reference retrieved. Re-write this function if you
        want to test more complicated QA process like Multi-Hop QAs.
        在这里，我们实现了单个 LLM 调用 w/ 或 w/o 引用检索的过程。如果您想要测试更复杂的 QA 流程，如多跳 QA。
        """
        reference_chunks: List[str] = self._retriever.retrieve_contents(qa, retrieve_id=f"Q{question_idx:03}")
        messages = self._qa_protocol.process_input(content=qa.question, references=reference_chunks, **qa.as_dict())

        response = self._client.generate_content_with_messages(messages, **self.llm_config)
        output_dict: dict = self._qa_protocol.parse_output(response, **qa.as_dict())

        if "response" not in output_dict:
            output_dict["response"] = response

        if "reference_chunks" not in output_dict:
            output_dict["reference_chunks"] = reference_chunks

        return output_dict
