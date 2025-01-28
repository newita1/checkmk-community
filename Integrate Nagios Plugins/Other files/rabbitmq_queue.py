import requests
import json
import warnings
from requests.auth import HTTPBasicAuth
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from cryptography.fernet import Fernet

def decrypt(name):
    # Ruta de la clave privada
    with open("/opt/scripts/encrypter/key.fernet", "rb") as f: 
        key = f.read()
        f.close()
    fernet = Fernet(key)
    # Ruta contraseña cifrada
    with open(f"/opt/scripts/encrypter/passwords/{name}.fernet", 'rb') as file:
        password = file.read()
    decrypted_password = fernet.decrypt(password)
    return decrypted_password.decode()

def get_data_rabbitmq(port=443):
    # Se pasan por linea de comando todos los argumentos
    host = sys.argv[1]
    vhost = sys.argv[2]
    queue = sys.argv[3]
    user= sys.argv[4]
    decrypt_pass = decrypt(sys.argv[5])

    if port != 443:
        # Se hace la query a la API, con authentication HTTPBasic y verify False (En caso de que salte problemas con el SSL)
        request = requests.get(f'http://{host}:{port}/api/queues/{vhost}/{queue}', auth=HTTPBasicAuth(user, decrypt_pass), verify=False)
    else:
        request = requests.get(f'https://{host}:{port}/api/queues/{vhost}/{queue}', auth=HTTPBasicAuth(user, decrypt_pass), verify=False)
    result = json.loads(request.text)

    try:
        # Antes del | es lo que se ve en Summary, lo que viene despues es para graficar.
        if int(result['messages']) > 1000 or int(result['messages_ready']) > 1000 or int(result['messages_unacknowledged']) > 1000: 
            print(f"RABBITMQ_OVERVIEW CRIT - messages({result['messages']}) messages_ready ({result['messages_ready']}) messages_unacknowledged ({result['messages_unacknowledged']}) consumers ({result['consumers']}) | messages={result['messages']} messages_ready={result['messages_ready']} messages_unacknowledged={result['messages_unacknowledged']} consumers={result['consumers']}")
            sys.exit(2)
        elif int(result['messages']) > 700 or int(result['messages_ready']) > 700 or int(result['messages_unacknowledged']) > 700:
            print(f"RABBITMQ_OVERVIEW WARN - messages({result['messages']}) messages_ready ({result['messages_ready']}) messages_unacknowledged ({result['messages_unacknowledged']}) consumers ({result['consumers']}) | messages={result['messages']} messages_ready={result['messages_ready']} messages_unacknowledged={result['messages_unacknowledged']} consumers={result['consumers']}")
            sys.exit(1)
        else:
            print(f"RABBITMQ_OVERVIEW OK - messages({result['messages']}) messages_ready ({result['messages_ready']}) messages_unacknowledged ({result['messages_unacknowledged']}) consumers ({result['consumers']}) | messages={result['messages']} messages_ready={result['messages_ready']} messages_unacknowledged={result['messages_unacknowledged']} consumers={result['consumers']}")
    except:
        print(f"No se obtiene respuesta de la API de la RabbitMQ")
        sys.exit(2)

    
if __name__ == '__main__':
    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
    try:
        get_data_rabbitmq(port=sys.argv[6])
    except:
        get_data_rabbitmq()
    
