import requests 
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO , format='%(levelname)s: %(message)s')

def Extraer_clientes ():
    url = "https://jsonplaceholder.typicode.com/users"
    try:
        logging.info("iniciando conexion a la API de clientes")
        req = requests.get(url)
        
        req.raise_for_status()
        
        data = req.json()
        logging.info(f"extraccion exitosa  se descargaron {len(data)} clientes.")
        return data
    except requests.exceptions.RequestException as error:
        logging.info(f"fallo en la conexion: {error}")
        return []

    
    
def transformar_data_y_guardar (datos_json):
    
    logging.info("empezando la transformacion con pandas")
    
    df = pd.json_normalize(datos_json)
    
    df_limpio = df[['name', 'email','address.city']]
    
    df_limpio= df_limpio.rename(columns={
        'name':'nombre_cliente',
        'email':'correo',
        'address.city': 'ciudad'
    })
    df_limpio= df_limpio[df_limpio['ciudad']=='Gwenborough'] 
    
    df_limpio= df_limpio.dropna(subset=['correo'])
    
    df_limpio.to_csv('cliente_logistica.csv', index=False)
    logging.info("pipeline finalizado")

if __name__ == "__main__":
    datos_crudos = Extraer_clientes()
    
    if datos_crudos:
        transformar_data_y_guardar(datos_crudos)