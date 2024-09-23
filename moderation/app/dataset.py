from sentence_transformers import SentenceTransformer
import pandas as pd
import psycopg2
from datasets import Dataset, load_dataset

class Datas():
    def __init__(self, db='', hf=''):
        # Load embedding model
        encoder_name = "Lajavaness/sentence-camembert-large"
        self.encoder = SentenceTransformer(encoder_name)
        print(f"[Done] Loaded encoder {encoder_name}: {self.encoder.max_seq_length} input size.")

        # Initialize dataset
        self.db = db
        self.hf = hf
        self.table = None
        self.datas = None
        print("[Done] Dataset initialized.")

    #################
    # Dataset methods
    #################
    def read(self, table=''):
        conn = psycopg2.connect(self.db)
        cur = conn.cursor()
        print("[Done] Connected to database.")

        # Load table
        self.table = table
        print(f"[Pending] Loading {table} table...")
        query = f"SELECT * FROM {table}"
        cur.execute(query)
        datapoints = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        self.datas = pd.DataFrame(datapoints, columns=cols)

        cur.close()
        print(f"[Done] {table} table loaded.")

    def prepare(self):
        if self.table == 'verbatims':
            cols = ['question_key', 'content', 'status', 'created_at']
            dataset = self.datas[cols].copy()
            dataset['text'] = dataset['question_key'] + ': ' + dataset['content']
            dataset['created_at'] = pd.to_datetime(dataset['created_at'])
            dataset['year'] = dataset['created_at'].dt.year
            dataset['month'] = dataset['created_at'].dt.month
            dataset['day'] = dataset['created_at'].dt.day
            dataset.drop(columns=['question_key', 'content', 'created_at'], inplace=True)
            dataset.drop_duplicates(inplace=True)
            dataset.reset_index(drop=True, inplace=True)
            self.datas = dataset
            print(f"[Done] {self.table} dataset ready.")
        else:
            print(f"[Error] Unknown specific format rules for {table} dataset.")

    def encode(self, text_col):
        # Create embeddings
        texts = self.datas[text_col].tolist()
        print(f"[Pending] Encoding dataset {self.table}...")
        try:
            embeddings = self.encoder.encode(texts, device="cuda", show_progress_bar=True)
        except:
            embeddings = self.encoder.encode(texts, device="cpu", show_progress_bar=True)
        emb_df = pd.DataFrame(embeddings)
        emb_df.columns = [f"emb_{i+1}" for i in range(emb_df.shape[1])]
        self.datas = pd.concat([self.datas, emb_df], axis=1)
        print(f"[Done] {self.table} embeddings ready.")

    def save(self, repo):
        dataset = Dataset.from_pandas(self.datas)
        dataset.push_to_hub(repo, private=True, token=self.hf)
        print(f"[Done] {self.table} exported to: {repo}.")

    def load(self, table, repo):
        self.table = table
        self.datas = load_dataset(repo, token=self.hf, split="all").to_pandas()
        print(f"[Done] {self.table} loaded from {repo}: {self.datas.shape}")