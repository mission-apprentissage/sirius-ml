from dataset import Datas
import os

# Instanciate dataset
datas = Datas(api=os.environ['SIRIUS_DB_API'], hf=os.environ['SIRIUS_HF_TOKEN'])

# Run training
table = os.environ['table']
repo = os.environ['repo']
print(f'[sirius-moderation] Updating SIRIUS {table} dataset...')

# Extract dataset from table
datas.read(table=table)
datas.prepare(table=table)
datas.encode(text_col='text')

# Export dataset
datas.save(repo=repo)
print(f"SIRIUS {table} dataset updated to {repo}.")