import requests
import json

def obtenertoken():
    url = "https:/url:51443/auth/token"

    # Datos necesarios para la autenticación
    api_key = "tu_apiKey"  # Reemplaza con tu apiKey
    api_secret = "tu_apiSecret"  # Reemplaza con tu apiSecret

    # Cabeceras HTTP
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Datos para el cuerpo de la solicitud
    data = {
        "apiKey": api_key,
        "apiSecret": api_secret
    }

    # Realizar la solicitud POST
    try:
        response = requests.post(url, headers=headers, data=data)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(response.json())
            return(response.json())
        else:
            print(f"Error al obtener el token. Código de estado: {response.status_code}")
            print("Respuesta:", response.text)

    except Exception as e:
        print("Ocurrió un error al realizar la solicitud:")
        print(str(e))

def generateuuid():
    url="https://url:51443/help/uuid"
    
    responseuuid = requests.get(url)
    responseuuid = json.loads(responseuuid.text)
    
    responseuuid = responseuuid["uuid"]
    return responseuuid

def sendsms(token):
    
    uuid = generateuuid()
    
    url = "https://url:51443/sms"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    
    payload = {
    "message": {
        "id": uuid,
        "text": "Test Comunica SMS",
        "sender": "CSMS",
        "mobile": "34600000001" 
        }
    # "settings": {
    #     "name": "Test API yyyy-MM-dd",
    #     "isCert": False,
    #     "isUnicode": False,
    #     "priority": 0
    #     }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response)
        
    except Exception as e:
        print(f"Error durante la solicitud: {e}")

if __name__ == "__main__":
    token = obtenertoken()
    sendsms(token)
    