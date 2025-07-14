## 这个项目的初衷是为了让初学者尽可能快的上手PIKE-RAG！

## 如何使用？
> 下载并解压文件后，您需要在huggingface下载一个开源的大模型，并放入myLLM文件夹下，再运行qa.py即可。


## 大模型配置
> 本项目测试时使用的是deepseek-coder-instruct-1.3b的模型，如果使用其他的模型可能需要修改pikerag\llm_client\local_deepseek_client.py下的代码

## 配置文件 
> 相关配置可以参考QA.yml文件下的注释。

## 如何配置参考文档？
> PIKR-RAG需要读取pkl文件作为参考文档，您可以参考以下格式进行文档生成：
```
from langchain_core.documents import Document
import pickle

chunks = [
    Document(
        page_content=(
            "门诊服务时间为周一至周五 08:00–17:00，节假日视安排调整。"
            "所有患者需携带有效身份证件挂号，挂号后根据导诊台引导前往相关科室。"
            "支持微信、支付宝、医保卡和现金缴费。"
        ),
        metadata={"filename": "hospital_guide.txt", "chunk_idx": 0}
    ),
    Document(
        page_content=(
            "预约挂号可提前 7 天，支持网上预约和自助机预约。"
            "预约成功后请在就诊当天提前 15 分钟签到。"
            "如需取消预约，须至少提前 1 天操作，过时无法退号。"
        ),
        metadata={"filename": "hospital_guide.txt", "chunk_idx": 1}
    ),
    Document(
        page_content=(
            "化验单、检查单可通过自助机或人工窗口打印。"
            "检查如心电图、B超多数无需特殊准备，特殊项目由医生告知是否空腹。"
            "药品可在门诊药房领取，需凭缴费凭证或处方单。"
        ),
        metadata={"filename": "hospital_guide.txt", "chunk_idx": 2}
    ),
]

with open("hospital_info.pkl", "wb") as fout:
    pickle.dump(chunks, fout)

```

## License

This project is a simplified version of [PIKE-RAG](https://github.com/microsoft/PIKE-RAG), originally developed by Microsoft and released under the MIT License.

Copyright (c) Microsoft Corporation  
Copyright (c) 2025 MrYangPengJu

This modified version is also released under the [MIT License](./LICENSE).
