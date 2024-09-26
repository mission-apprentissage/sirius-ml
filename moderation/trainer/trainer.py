from dataset import Datas
import os
from ipwhois import IPWhois
from requests import get

def main():
    # Instanciate dataset
    datas = Datas(db=os.environ['SIRIUS_DB_URL'], hf=os.environ['SIRIUS_HF_TOKEN'])

    # Get IP adress for database connection
    ip = get('https://api.ipify.org').text
    whois = IPWhois(ip).lookup_rdap(depth=1)
    cidr = whois['network']['cidr']
    name = whois['network']['name']
    print('Provider:  ', name)
    print('Public IP: ', ip)
    print('CIDRs:     ', cidr)

    # Run training
    table = os.environ['table']
    repo = os.environ['repo']
    print(f'[sirius-moderation] Updating SIRIUS {table} dataset...')

    # Extract dataset from table
    datas.read(table=table)
    datas.prepare()
    datas.encode(text_col='text')

    # Export dataset
    datas.save(repo=repo)

    return {"status": f"SIRIUS {table} dataset updated to {repo}."}

if __name__ == "__main__":
    main()