#!/usr/bin/env python3
import pprint
import requests
import pandas as pd
from tqdm import tqdm
import os

HOST_NAME = "localhost"
SITE_NAME = "site"
API_URL = f"http://{HOST_NAME}/{SITE_NAME}/check_mk/api/1.0"

HEADERS = {"Authorization": "Bearer usuario contrasena ", "Accept": "application/json", "Content-Type": "application/json"}

session = requests.session()
session.headers = HEADERS

def add_service_groups(name, alias):
    resp = session.post(
        f"{API_URL}/domain-types/host_group_config/collections/all",
        headers={
            "Content-Type": 'application/json',  # (required) A header specifying which type of content is in the request/response body.
        },
        json={
            'name': name,
            'alias': alias
        },
    )
    if resp.status_code == 200:
        pprint.pprint(resp.json())
    elif resp.status_code == 204:
        print("Done")
    else:
        raise RuntimeError(pprint.pformat(resp.json()))

if __name__ == '__main__':
    # Solicitamos en un input los hosts a los que se les va a realizar la modificación
    data_frame = pd.read_excel('list_hostgroups.xlsx')
    os.system('cls')  # Limpia la pantalla, puede variar según el sistema operativo

    if not data_frame.empty:
        for index, row in tqdm(data_frame.iterrows(), desc="Agregando host groups"):
            add_service_groups(*row.values)
    else:
        print("El DataFrame está vacío.")
