import requests
import json
import re
import time
import pandas as pd
from tqdm import tqdm #Requiere instalacion
import os
#Definimos variables generales
headers = {"Authorization": "Bearer usuario contrasena ","Accept": "application/json","Content-Type": "application/json"}
etag = ""

#Obtenemos el etag del host para poder modificarlo posteriormente, si no existe el etag significa que el host al que se esta atacando no existe, devolvemos un "failed" para realizar el filtrado de los que SI tienen etag.
def getetag(hostname):
    #Declaramos las variables de la peticion.
    global etag
    global headers
    url = "http://url/slave/check_mk/api/1.0/objects/host_config/" + hostname
    #Mandamos la peticion.
    request = requests.get(url, headers=headers,verify=False)
    if request.status_code != 200:
        etag = ""
        return("failed")
    else:
        #Recogemos el valor de la peticion.
        return(request.headers.get("ETag"))

#Modificamos los hosts que tienen etag a traves de una request a la API
def modify_host_checkmk(etag, hostname, new_name):
    #Declaramos las variables de la peticion.
    url = f"http://url/slave/check_mk/api/v0/objects/host_config/{hostname}/actions/rename/invoke"
    headers = {"Authorization": "Bearer usuario contrasena ", "If-Match": etag ,"Accept": "application/json","Content-Type": "application/json", }
    data=json.dumps({
        "new_name": new_name
    })
    #Mandamos la peticion.
    request = requests.put(url, headers=headers, data=data, verify=False)
    if request.status_code != 200:
        print(request.text)
    #Aplicamos los cambios.
    url = "http://url/slave/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke"
    requests.post(url, headers=headers)
    
#Aplica los cambios realizados en CheckMK   
def apply_changes():
    global headers
    body = {
    "force_foreign_changes": "true"
    }
    request = requests.post("http://url/slave/check_mk/api/v0/domain-types/activation_run/actions/activate-changes/invoke", headers=headers, verify=False, data=json.dumps(body), timeout=60)
    print(request.text)


if __name__ == '__main__':
    #Solicitamos en un input los hosts a los que se les va a realizar la modificacion
    data_frame = pd.read_excel('modificar_nombre.xlsx')
    os.system('cls')
    for index, row in tqdm(data_frame.iterrows(), desc="Modificando nombre"):
        etag = getetag(row.values[0])
        if not "failed" in str(etag):
            modify_host_checkmk(str(etag), row.values[0],row.values[1])
            time.sleep(140)
            apply_changes()
            time.sleep(300)
        try:
            modify_host_checkmk(str(etag), row.values[0],row.values[1])
            time.sleep(140)
            apply_changes()
            time.sleep(300)
        except:
            continue  

    #Una vez todos los hosts se han modificado se llama a la funcion "apply_changes" para aplicar los cambios
    
        