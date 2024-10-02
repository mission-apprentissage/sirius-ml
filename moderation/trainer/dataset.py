from sentence_transformers import SentenceTransformer
import pandas as pd
import requests
from datasets import Dataset, load_dataset
from joblib import Parallel, delayed
from tqdm import tqdm
from multiprocessing import cpu_count

class Datas():
    def __init__(self, api='', hf=''):
        # Load embedding model
        encoder_name = "Lajavaness/sentence-camembert-large"
        self.encoder = SentenceTransformer(encoder_name)
        print(f"[Done] Loaded encoder {encoder_name}: {self.encoder.max_seq_length} input size.")

        # Initialize dataset
        self.api = api
        self.hf = hf
        self.datas = None
        print("[Done] Dataset initialized.")

    #################
    # Dataset methods
    #################
    def read(self, table=''):
        payload = dict(
            table = table        
        )
        resp = requests.post(url=self.api, json=payload)
        data = resp.json()
        self.datas = pd.DataFrame(data['datapoints'], columns=data['cols'])
        print(f"[Done] Dataset loaded.")

    def prepare(self, table=''):
        if table == 'verbatims':
            cols = ['question_key', 'content', 'status', 'created_at']
            dataset = self.datas[cols].copy()
            dataset['text'] = dataset['question_key'] + ': ' + dataset['content']
            dataset['created_at'] = pd.to_datetime(dataset['created_at'], format='ISO8601')
            dataset['year'] = dataset['created_at'].dt.year
            dataset['month'] = dataset['created_at'].dt.month
            dataset['day'] = dataset['created_at'].dt.day
            dataset.drop(columns=['question_key', 'content', 'created_at'], inplace=True)
            dataset.drop_duplicates(inplace=True)
            dataset.reset_index(drop=True, inplace=True)
            self.datas = dataset
            print(f"[Done] Dataset prepared.")
        else:
            print(f"[Error] Unknown specific format rules for {table} dataset.")

    def encode(self, text_col):
        # Create embeddings
        texts = self.datas[text_col].tolist()
        print(f"[Pending] Encoding dataset...")
        try:
            embeddings = self.encoder.encode(texts, device="cuda", show_progress_bar=True)
        except:
            nb_cpu = min(cpu_count(), 8)
            embeddings = Parallel(n_jobs=nb_cpu - 1, prefer="threads")(delayed(self.encoder.encode)(i) for i in tqdm(texts, desc=f"Encoding on {nb_cpu} CPU"))

        emb_df = pd.DataFrame(embeddings)
        emb_df.columns = [f"emb_{i+1}" for i in range(emb_df.shape[1])]
        self.datas = pd.concat([self.datas, emb_df], axis=1)
        print(f"[Done] Embeddings ready.")

    def save(self, repo):
        dataset = Dataset.from_pandas(self.datas)
        dataset.push_to_hub(repo, private=True, token=self.hf)
        print(f"[Done] Dataset exported to: {repo}.")

    def load(self, repo):
        self.datas = load_dataset(repo, token=self.hf, split="all").to_pandas()
        print(f"[Done] Dataset loaded from {repo}: {self.datas.shape}")