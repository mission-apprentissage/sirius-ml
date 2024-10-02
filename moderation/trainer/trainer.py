from dataset import Datas
import os
from ipwhois import IPWhois
from requests import get

def main():
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

    return {"status": f"SIRIUS {table} dataset updated to {repo}."}

if __name__ == "__main__":
    main()