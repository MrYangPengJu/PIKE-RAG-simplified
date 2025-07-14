from typing import Any, List, Dict
from pikerag.llm_client.base import BaseLLMClient

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class LocalDeepSeekClient(BaseLLMClient):
    NAME = "LocalDeepSeekClient"

    def __init__(self, location: str = None, auto_dump: bool = True, logger=None,
                 llm_config: dict = None, **kwargs):
        super().__init__(location=location, auto_dump=auto_dump, logger=logger, **kwargs)

        llm_config = llm_config or {}
        self.model_path = llm_config.get("model_path", "./myModels")
        self.temperature = llm_config.get("temperature", 0.7)
        self.max_new_tokens = llm_config.get("max_new_tokens", 1024)

        print(f"[INFO] 正在加载本地模型 {self.model_path}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            trust_remote_code=True,
        )
        self.model.eval()

    def _get_response_with_messages(self, messages: List[dict], **llm_config) -> Any:
        prompt = self._format_messages_to_prompt(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                do_sample=False,
                temperature=self.temperature,
                max_new_tokens=self.max_new_tokens,
            )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

    def _get_content_from_response(self, response: str, messages: List[dict] = None) -> str:
        prompt = self._format_messages_to_prompt(messages)
        return response[len(prompt):].strip()

    def _format_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        将多轮 message 组合成一个符合 DeepSeek 格式的 prompt 字符串。
        不修改 message 内容，仅添加 <|role|>\n 前缀。
        """
        prompt = ""
        for msg in messages:
            role = msg.get("role", "").strip()
            content = msg.get("content", "").strip()

            if role == "system":
                prompt += f"<|system|>\n{content}\n"
            elif role == "user":
                prompt += f"<|user|>\n{content}\n"
            elif role == "assistant":
                prompt += f"<|assistant|>\n{content}\n"

        # 最后引导模型继续 assistant 角色
        prompt += "<|assistant|>\n"
        return prompt



    # def _format_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
    #     prompt = ""
    #     for msg in messages:
    #         role = msg.get("role")
    #         content = msg.get("content", "").strip()

    #         if role == "system":
    #             prompt += f"<|system|>\n{content}\n"
    #         elif role == "user":
    #             prompt += (
    #                 "<|user|>\n"
    #                 "请将以下文本切分成两部分，并用特定的 XML 格式输出，"
    #                 "格式必须包含顶层 <result> 标签，和两个 <chunk> 标签，每个 <chunk> 中包含 <endline> 和 <summary>，示例如下：\n\n"
    #                 "<result>\n"
    #                 "  <chunk>\n"
    #                 "    <endline>10</endline>\n"
    #                 "    <summary>第一部分摘要内容</summary>\n"
    #                 "  </chunk>\n"
    #                 "  <chunk>\n"
    #                 "    <endline>20</endline>\n"
    #                 "    <summary>第二部分摘要内容</summary>\n"
    #                 "  </chunk>\n"
    #                 "</result>\n\n"
    #                 "以下是待切分的文本：\n"
    #                 f"{content}\n"
    #             )
    #         elif role == "assistant":
    #             prompt += f"<|assistant|>\n{content}\n"

    #     prompt += "<|assistant|>\n"
    #     return prompt


