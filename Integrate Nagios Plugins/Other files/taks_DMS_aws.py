import sys
import subprocess
import json

dms_tasks = sys.argv[1]  # Pasar las tasks de dms

# Comando para obtener las tareas, variables nombre, errores y estado
comando = f"aws dms describe-replication-tasks | jq -c '[.ReplicationTasks[] | select(.ReplicationTaskIdentifier | contains(\"{dms_tasks}\")) | {{ReplicationTaskIdentifier: .ReplicationTaskIdentifier, Status: .Status, TablesErrored: .ReplicationTaskStats.TablesErrored}}]'"

#Ejecutar comando y dar formato
resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
tareas = resultado.stdout.strip()
tareas_json = []

if tareas:
    # Separar cada objeto JSON en líneas
    tareas_json = tareas.split('\n')

diccionario = []
for tarea in tareas_json:
    if tarea:  # Asegurarse de que la línea no esté vacía
        try:
            diccionario.append(json.loads(tarea))
        except json.JSONDecodeError as e:
            print(f"Error {e}")

if len(diccionario) == 1 and isinstance(diccionario[0], list):
    diccionario = diccionario[0]

for tarea in diccionario:
    identificador = tarea['ReplicationTaskIdentifier']
    status = tarea['Status']
    tables_errored = tarea['TablesErrored']

    if status == "running" and tables_errored == 0:
        print(f"DMS {identificador} - Status: {status} - TablesErrored: {tables_errored}")
        sys.exit(0)
    else:
        print(f"DMS {identificador} - Status: {status} - TablesErrored: {tables_errored}")
        sys.exit(2)
