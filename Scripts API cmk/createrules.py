#!/usr/bin/env python3
#import pprint
import requests
import pandas as pd
import sys
HOST_NAME = ""
SITE_NAME = ""
API_URL = f"http://{HOST_NAME}/{SITE_NAME}/check_mk/api/1.0"

USERNAME = ""
PASSWORD = ""
EXCEL_PATH = sys.argv[2]
FOLDER = sys.argv[1]

def readCommand(path):
    data = pd.read_csv(path, delimiter=';')
    #print(data.loc['host_name'])
    for index, row in data.iterrows():
        # Obtenemos los hosts de la celda y los convertimos en una lista, separando por coma
        hostnames = row['host'].split(',')  # Genera una lista con todos los hosts, separándolos por comas

        service_name = row['Description']
        command = row['Command']
    
        command_line = {
            'command_line': command,
            'has_perfdata': True,
            'service_description': service_name
        }

        # Iteramos sobre cada host en la lista de hosts
        createRule(command_line, hostnames)

def createRule(command_line,host):

    session = requests.session()
    session.headers['Authorization'] = f"Bearer {USERNAME} {PASSWORD}"
    session.headers['Accept'] = 'application/json'
    resp = session.post(
        f"{API_URL}/domain-types/rule/collections/all",
        headers={
            "Content-Type": 'application/json',  # (required) A header specifying which type of content is in the request/response body.
        },
        json={
            'ruleset': 'custom_checks',
            'folder': FOLDER,
            'properties': {
                'disabled': False
            },
            'value_raw': str(command_line),
            'conditions': { "host_name": {
                            "match_on": host,
                            "operator": "one_of"
                        },
                        }
        },
    )

    
readCommand(EXCEL_PATH)