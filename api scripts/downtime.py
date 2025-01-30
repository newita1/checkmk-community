import requests
import pandas as pd
from tqdm import tqdm
import re
import os

# Definimos variables generales
API_URL = "http://host/slave/check_mk/api/1.0/"
HEADERS = {"Authorization": "Bearer usuario contraseña ", "Accept": "application/json", "Content-Type": "application/json"}

# Inicializamos la sesión
session = requests.session()
session.headers = HEADERS

# Modificamos los hosts que tienen etag a través de una request a la API
def add_host_checkmk(hostname):
    try:
        resp = session.post(
            f"{API_URL}/domain-types/downtime/collections/host",
            headers={
                "Content-Type": 'application/json',  # (required) A header specifying which type of content is in the request/response body.
            },
            # This schema has multiple variations. Please refer to
            # the 'Payload' section for details.
            json={
                'start_time': '2024-03-18T3:00:00Z',
                'end_time': '2024-03-18T9:00:00Z',
                'recur': 'fixed',
                'comment': 'Downtime por solicitud de cambio',
                'downtime_type': 'host',
                'host_name': hostname
            },
        )

        if resp.status_code == 200:
            print("OLEE 200")
        elif resp.status_code == 204:
            print("OLEE 204")
    except:
        print("error =>" + TypeError )


if __name__ == '__main__':
    #Solicitamos en un input los hosts a los que se les va a realizar la modificacion
    hosts = input("Listado de hosts que van a ser modificados: \n")
    #Spliteamos el resultado para obtener una lista con todos los hosts como valores
    hosts = hosts.split(",")
    os.system('cls')
    for i in tqdm(hosts, desc="Getting information from host"):
        i = re.sub(" ","", i)
        add_host_checkmk(i)
         
