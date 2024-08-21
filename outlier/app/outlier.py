import pandas as pd
import json
import os
from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.mixture import GaussianMixture
from io import BytesIO
import ast

data_path = './dataset/'

class Outlier:
    def __init__(self):
        # Load embedding model
        model_name = "Lajavaness/sentence-camembert-large"
        self.encoder = SentenceTransformer(model_name)
        print(f"Loaded model {model_name} ({self.encoder.max_seq_length} tokens)")

    def fit(self, file_id):
        # Load dataframe
        file_path = data_path + file_id + '.csv'
        datas_df = pd.read_csv(file_path, na_filter=False, low_memory=False)
        print(f"Loaded dataset {datas_df.shape}.")

        # Filter on categorical features
        num_feat = [col for col in datas_df.columns if datas_df[col].dtype == int]
        txt_feat = [col for col in datas_df.columns if col.endswith(('content', 'Conseil', 'Autre'))]
        cat_feat = [col for col in datas_df.columns if col not in num_feat + txt_feat]
        print(f"- Numerical features: {len(num_feat)}")
        print(f"- Categorical features: {len(cat_feat)}")
        print(f"- Text features: {len(txt_feat)}")

        # Encode features
        num_df = datas_df[num_feat]
        cat_df = pd.concat([pd.get_dummies(datas_df[col], prefix=col, dummy_na=False, dtype=int) for col in cat_feat], axis=1)

        # Start the multi-process pool on all available CPU
        #print(f"Start multi-process pool...")
        #pool = self.encoder.start_multi_process_pool(["cpu"]*4)
        print(f"Start encoding sentences...")
        # Compute the embeddings using the multi-process pool
        text_df = pd.concat([pd.DataFrame(self.encoder.encode(datas_df[col], show_progress_bar=True)) for col in txt_feat], axis=1)
        #text_df = pd.concat([pd.DataFrame(self.encoder.encode_multi_process(datas_df[col], pool, show_progress_bar=True)) for col in txt_feat], axis=1)
        # Optional: Stop the processes in the pool
        #self.encoder.stop_multi_process_pool(pool)

        txt_cols = []
        for col in txt_feat:
            for i in range(1024):
                txt_cols.append(col.split('.')[1]+'_'+str(i+1))
        text_df.columns = txt_cols
        dataset = pd.concat([num_df, cat_df, text_df], axis=1)
        print(f"Encoded dataset {dataset.shape}.")

        # PCA optimization
        pca = PCA()
        sc = StandardScaler()
        X_std = sc.fit_transform(dataset)
        X_pca = pca.fit_transform(X_std)
        threshold = 0.99
        features = 0
        v = 0
        exp_var_pca = pca.explained_variance_ratio_
        cum_sum_eigenvalues = np.cumsum(exp_var_pca)
        while v < threshold:
            v = cum_sum_eigenvalues[features]
            features+=1
        X_train = X_pca[:, :features]
        train_ds = pd.DataFrame(X_train)
        print(f"Reduced PCA dataset {train_ds.shape}.")

        # Compute TSNE
        matrix = np.array(train_ds) # Convert to a list of lists of floats
        tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
        vis_dims = tsne.fit_transform(matrix)
        print(f"Computed TSNE dataset {vis_dims.shape}.")

        # Train GaussianMixture model
        model = GaussianMixture(n_components=2, random_state=42)
        model.fit(vis_dims)
        print(f"Trained GaussianMixture model.")

        # Get the score for each sample
        train_ds = pd.DataFrame(vis_dims)
        scores = model.score_samples(train_ds)
        print(f"Scored dataset {len(scores)}.")
        return list(scores)

def upload_dataset(bytes_data, file_id):
    datas_df = pd.read_csv(BytesIO(bytes_data))
    file_path = data_path + file_id + '.csv'
    datas_df.to_csv(file_path, index=False)
    print(f"Uploaded dataset {datas_df.shape} to {file_path}.")

def delete_dataset(file_id):
    file_path = data_path + file_id + '.csv'
    os.remove(file_path)
    print(f"Deleted dataset {file_path}.")

def normalize_dataset(file_id):
    pd.options.mode.chained_assignment = None  # default='warn'
    def literal_eval(val):
        try:
            return ast.literal_eval(val)
        except:
            return val

    def normalize_list(samples, col):
        return pd.get_dummies(samples.explode(), prefix=col, prefix_sep='.').groupby(level=0).sum()

    def normalize_dict(samples, col):
        def clean_dict(sample):
            try:
                norm = pd.json_normalize(sample, errors='ignore').T
                cols = norm.iloc[0].values
                vals = norm.iloc[1].values
                norm_df = pd.DataFrame({col:[val] for col, val in zip(cols, vals)})
                return norm_df
            except:
                return pd.DataFrame()

        def clean_cols(samples):
            cols = set()
            for sample in samples:
                cols.update(list(sample.columns))

            for i in range(len(samples)):
                if len(samples[i]) == 0:
                    samples[i] = pd.DataFrame({col:['-'] for col in cols})
            return samples

        norms = [clean_dict(val) for val in samples]
        norms = clean_cols(norms)
        return pd.concat(norms, ignore_index=True).add_prefix(col+'.', axis=1)

    def normalize(df):
        res = []
        for col in df.columns:
            # print(f"- Normalizing column {col}...")
            serie = df[col].apply(literal_eval)

            # Check if list type
            if any(serie.apply(lambda x: isinstance(x, list))):
                try:
                    # List type
                    res.append(normalize_list(serie, col))
                except:
                    # List of dict type
                    res.append(normalize_dict(serie.apply(literal_eval).fillna(''), col))
            else:
                res.append(serie)
        return pd.concat(res, axis=1)

    file_path = data_path + file_id + '.csv'
    datas_df = pd.read_csv(file_path).apply(literal_eval)

    # Normalize dataset
    norm_df = normalize(datas_df)
    norm_df.to_csv(file_path, index=False)
    print(f"Normalized dataset {norm_df.shape}.")