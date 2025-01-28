import requests
from datetime import datetime, timedelta
import os
import json
import time
from collections import defaultdict
import sys

# Definir el endpoint de Velocloud y el token de autenticación
VELOCLOUD_URL = "https://url/portal/"
VELOCLOUD_TOKEN = "Token xxx"
OMD_ROOT = os.getenv('OMD_ROOT')
OMD_SITE = sys.argv[1]

# Definir los mapeos de estado
EDGE_STATE_MAPPING = {
    'CONNECTED': 1,
    'DISCONNECTED': 0,
}

current_time_ms = int(datetime.utcnow().timestamp() * 1000)
current_time_seconds = int(datetime.utcnow().timestamp())
minutes_15_ago_ms = current_time_ms - (15 * 60 * 1000)

LINK_STATE_MAPPING = {
    'UP': 1,
    'DOWN': 0,
}

def link_metric_data(curr_timestmap, min_15_ago_timestamp):
    headers = {
        "Content-Type": "application/json",
        "Authorization": VELOCLOUD_TOKEN
    }

    body = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "monitoring/getAggregateEdgeLinkMetrics",
        "params": {
            "interval": {
                "start": min_15_ago_timestamp,
                "end": curr_timestmap
            }
        }
    }

    # Hacer la solicitud a Velocloud
    response = requests.post(VELOCLOUD_URL, json=body, headers=headers)

    return response.json()['result']

class State:
    WARN = 'warn'
    CRIT = 'crit'
    OK = 'ok'
    UNKNOWN = 'unknown'

_velocloud_map_vpn_state = {
    'INITIAL': (State.WARN, '1'),
    'DEAD': (State.CRIT, '2'),
    'UNUSABLE': (State.CRIT, '3'),
    'QUIET': (State.WARN, '4'),
    'STANDBY': (State.OK, '5'),
    'UNSTABLE': (State.WARN, '6'),
    'STABLE': (State.OK, '7'),
    'UNKNOWN': (State.CRIT, '8'),
    'DISCONNECTED': (State.CRIT, '2'),
}

def is_disconnected_for_30_days(last_activity):
    last_activity_date = datetime.strptime(last_activity, "%Y-%m-%dT%H:%M:%S.%fZ")
    current_date = datetime.utcnow()
    return (current_date - last_activity_date) > timedelta(days=30)

def get_edge_link_status():
    headers = {
        "Content-Type": "application/json",
        "Authorization": VELOCLOUD_TOKEN
    }

    body = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "monitoring/getEnterpriseEdgeLinkStatus",
        "params": {
            "enterpriseId": 1281,
            "links": True,
            "detailed": True
        }
    }

    # Hacer la solicitud a Velocloud
    response = requests.post(VELOCLOUD_URL, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()['result']
        metrics_data = link_metric_data(current_time_ms, minutes_15_ago_ms)
        # Procesar cada resultado de edge y link
        links_array = []
        for edge in data:
            name = edge['edgeName']
            state = edge['linkState']
            interface = edge['interface']
            state_num = _velocloud_map_vpn_state.get(state, (State.UNKNOWN, '-1'))[1]
            link_name = edge['displayName']
            isp = edge['isp']
            last_activity = edge['linkLastActive']
            bytesRx = 0
            bytesTx = 0
            scoreRx = 0
            scoreTx = 0
            bestJitterMsRx = 0
            bestJitterMsTx = 0
            bestLatencyMsRx = 0
            bestLatencyMsTx = 0
            for edge_metrics in metrics_data:
                if edge['displayName'] == edge_metrics['link']['displayName'] and edge['edgeName'] == edge_metrics['link']['edgeName']:
                    bytesRx = edge_metrics['bytesRx']
                    bytesTx = edge_metrics['bytesTx']
                    scoreRx = edge_metrics['scoreRx']
                    scoreTx = edge_metrics['scoreTx']
                    bestJitterMsRx = edge_metrics['bestJitterMsRx']
                    bestJitterMsTx = edge_metrics['bestJitterMsTx']
                    bestLatencyMsRx = edge_metrics['bestLatencyMsRx']
                    bestLatencyMsTx = edge_metrics['bestLatencyMsTx']
                    
            if last_activity==None:
                pass
            elif is_disconnected_for_30_days(last_activity):
                pass
            else:
                links_array.append({
                    "name": name,
                    "state": state,
                    "interface": interface,
                    "state_num": state_num,
                    "link_name": link_name,
                    "isp": isp,
                    "last_activity": last_activity,
                    "metrics": {
                        "bytesRx": bytesRx,
                        "bytesTx": bytesTx,
                        "scoreRx": scoreRx,
                        "scoreTx": scoreTx,
                        "bestJitterMsRx": bestJitterMsRx,
                        "bestJitterMsTx": bestJitterMsTx,
                        "bestLatencyMsRx": bestLatencyMsRx,
                        "bestLatencyMsTx": bestLatencyMsTx
                    }
                })
        return links_array

    else:
        print(f"Error {response.status_code}: {response.text}")

def group_by_edge(data):
    gruped = defaultdict(list)
    
    for item in data:
        gruped[item['name']].append(item)
    
    # Convertimos el defaultdict a un diccionario normal y lo formateamos a JSON
    return {name: items for name, items in gruped.items()}
    # return json.dumps(result, indent=4)
    # return result

def generate_piggybackdatafile(json_data):
    if not OMD_ROOT:
        raise EnvironmentError("La variable de entorno 'OMD_ROOT' no está definida.")
    
    for to_host, entries in json_data.items():
        # Definir la ruta del archivo de piggyback
        pre_directory = os.path.join(OMD_ROOT, 'tmp', 'check_mk', 'piggyback', to_host.lower())
        piggy_path = os.path.join(OMD_ROOT, 'tmp', 'check_mk', 'piggyback', to_host.lower(), OMD_SITE)
        if not os.path.exists(pre_directory):
            os.makedirs(pre_directory)

        # Procesar cada entrada para el host
        content = f"<<<velocloud_links:sep(59)>>>\n"
        for entry in entries:
            state = entry['state_num']
            link_interface = entry['interface']
            isp = entry['isp']
            metrics = entry['metrics']
            last_activity = entry['last_activity']
                    
            # Crear el contenido del archivo de piggyback
            content += f"{state};{link_interface};{isp};" + ";".join([f"{clave}={valor}" for clave, valor in metrics.items()]) + "\n"
        
        
        # print(content)
        # time.sleep(5)
            # Guardar el contenido en el archivo
            # archivo_salida = os.path.join(piggy_path, f"{to_host}.txt")ll
        with open(piggy_path, 'w') as file:
            file.write(content)
            file.close()
        

def main():
    links_gruped = group_by_edge(get_edge_link_status())
    generate_piggybackdatafile(links_gruped)
    
    
if __name__ == "__main__":
    main()