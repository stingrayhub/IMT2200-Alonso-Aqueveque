import requests
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

''' Se agrega '''

from datetime import datetime, timedelta


def get_por_fecha( url,sesion):

    params = {
        'sppLocale': 'es_CL'
    }

    try:
        response = sesion.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        print("HTTPError:", e)
        return None
    except requests.exceptions.Timeout:
        print("Timeout alcanzado.")
        return None
    except requests.exceptions.RequestException as e:
        print("Error de red:", e)
        return None


api_key='lgttrn4k5g65'


'''Desde el 1 de enero de 2022 hasta el 31 de julio de 2025'''

inicio=datetime(year=2022, month=1, day=1)
fin=datetime(year=2025,month=7,day=31)
sesion=requests.Session()
sesion.headers.update({'X-eBirdApiToken': api_key})

fecha=inicio
tot_avistamientos=[]
while fecha <= fin:
    url = f"https://api.ebird.org/v2/data/obs/CL/historic/{fecha.year}/{fecha.month}/{fecha.day}"
    avistamientos_dia=get_por_fecha(api_key=api_key,url=url, sesion=sesion)
    if avistamientos_dia:
        print(len(avistamientos_dia))
        if tot_avistamientos:
            for avistamiento in avistamientos_dia:
                tot_avistamientos.append(avistamiento)
            print(f'{fecha} agregado a la lista')
            print(len(tot_avistamientos))
        else:
            tot_avistamientos=avistamientos_dia
            print(len(tot_avistamientos))
            print(len(avistamientos_dia))
            print(f'Primer elemento {fecha}')
    else:
        print('dia sin avistamientos (sus)')

    fecha+= timedelta(days=1)


df=pd.DataFrame(tot_avistamientos)

df.to_csv("avistamientos_chile.csv", index=False, encoding='utf-8')