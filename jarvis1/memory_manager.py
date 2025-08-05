from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os
import pickle

class SemanticMemory:
    def __init__(self, index_path="memory_index"):
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.index_path = index_path

        if os.path.exists(f"{index_path}/index.faiss"):
            with open(f"{index_path}/index.pkl", "rb") as f:
                self.db = pickle.load(f)
        else:
            self.db = FAISS.from_texts(["Jarvis booted up."], self.embeddings)
            self.save_index()

    def save_index(self):
        self.db.save_local(self.index_path)
        with open(f"{self.index_path}/index.pkl", "wb") as f:
            pickle.dump(self.db, f)

    def add_memory(self, text: str):
        self.db.add_texts([text])
        self.save_index()

    def recall(self, query: str):
        results = self.db.similarity_search(query, k=3)
        return [r.page_content for r in results]
