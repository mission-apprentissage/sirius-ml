from dataset import Datas
import os

print(f"SIRIUS training job started.")

# Instanciate dataset
datas = Datas(api=os.environ['SIRIUS_DB_API'], hf=os.environ['SIRIUS_HF_TOKEN'])

# Run training
table = os.environ['table']
repo = os.environ['repo']

# Extract dataset from table
datas.read(table=table)
datas.prepare(table=table)
datas.encode(text_col='text')

# Export dataset
datas.save(repo=repo)

print(f"SIRIUS training job ended.")