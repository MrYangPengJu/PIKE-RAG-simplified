# my_project/my_utils.py
import jsonlines
from typing import List
from pikerag.workflows.common import GenerationQaData

def load_open_qa_dataset(path: str) -> List[GenerationQaData]:
    data = []
    with jsonlines.open(path, "r") as reader:
        for sample in reader:
            data.append(
                GenerationQaData(
                    question=sample["question"],
                    answer_labels=sample["answer_labels"],
                    metadata=sample.get("metadata", {}),
                )
            )
    return data

# my_utils.py
from typing import Tuple, List, Literal
from langchain_core.documents import Document
import pickle, os

def load_ids_and_chunks(chunk_file_dir: str) -> Tuple[Literal[None], List[Document]]:
    all_chunks = []
    chunk_idx = 0

    for fname in os.listdir(chunk_file_dir):
        if not fname.endswith(".pkl"):
            continue
        with open(os.path.join(chunk_file_dir, fname), "rb") as f:
            docs: List[Document] = pickle.load(f)
            for doc in docs:
                doc.metadata.update({"filename": fname, "chunk_idx": chunk_idx})
                chunk_idx += 1
            all_chunks.extend(docs)

    return None, all_chunks
