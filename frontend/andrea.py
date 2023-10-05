import streamlit as st
import pandas as pd
import streamlit_option_menu
from streamlit_option_menu import option_menu
from PIL import Image
import psycopg2
from datetime import datetime
import random
import requests
import json
import os
#import db

from google.cloud import firestore

API_ENDPOINT = os.environ.get("API_ENDPOINT", "http://localhost:8080")
user = "andrea"


#prediccion
def call_api_predict_method(link):
    request_data = [{"link": link}]
    
    request_data_json = json.dumps(request_data)
    headers = {'Content-Type': 'application/json'}
    
    print(request_data_json)
    predict_method_endpoint = f"{API_ENDPOINT}/scrapper/predict"
    response = requests.request("POST",predict_method_endpoint , headers=headers, data=request_data_json)
    response_json = response.json()
    label = response_json
    return label

#estructura inicial de la app
def estructure():
    
    st.set_page_config(page_title="LinkScribe (◉‿◉)")
    
    # Título de la aplicación
    st.markdown("<h1 style='text-align: center;'>ENLACE FACIL</h1>", unsafe_allow_html=True)
    st.sidebar.image("andrea.gif")
    
    
        # Informacion del modelo
    with st.sidebar:
        selected = option_menu(
        menu_title = "Control del Modelo",
        options = ["Modelo"],
        icons = ["book"],
        menu_icon = "cloud",
        default_index = 0,)

    # codigo para el MODELO 
    if selected=="Modelo":
        
        st.sidebar.subheader("Descripción del Modelo")
        #meticas y como se realizo el modelo 1
        st.sidebar.write("Aquí puedes escribir la descripción del Modelo.")
        
     # Crear pestañas
    tabs = st.tabs(["APPY", "BIBILOTECA",])

    return(tabs)

#clasificacion usando el modelo
def LinkScribe(tabs):
    label=[]
    # Contenido de la pestaña "APPY"
    with tabs[0]:
        
        # Título de la subpágina
        st.markdown("<h1 style='text-align:;'>LinkScribe</h1>", unsafe_allow_html=True)
        
        # Entrada de enlace
        link = st.text_input("Ingresa un enlace:", "")
        submit_button = st.button("Procesar Enlace")

        #verificamos
        if submit_button:
            if link:
                      
                label=call_api_predict_method(link)
                
                st.subheader("Categoria:",)
                st.write(str(label[0]).upper()) 
                
                values = list(label)
                st.subheader("Título de la pagina:")
                st.write(str(label[2][0]).upper()) 

                st.subheader("Descripción:")
                st.write(str(label[1]))
                
                st.subheader("LINK:")
                st.write(link) 
                
                st.subheader("imagen de vista previa:")
                st.write("")
                st.image(label[3], caption="Image caption")
                
                submit_button = st.button("guardar datos")    
                if submit_button:
                    
                    #ccreamos diccionario para la base de datos
                    mi_diccionario = {
                                    'categoria': label[0],
                                    'descripcion': label[1],
                                    'titulo':label[2],
                                    'imagen':label[3],
                                    'link':link
                                    }
                   # db.guardar_datos(mi_diccionario,user)
                    
            # Aquí puedes agregar la lógica para procesar el enlace después de hacer clic en el botón
            else:
                # Mensaje de error  ingresó una URL
                st.markdown("<p style='color: red;'>Por favor, ingresa una URL.</p>", unsafe_allow_html=True)
    return(label,)

#comunicacion con la base de datos
#def baseDatos(tabs):
     #with tabs[1]:
        #db.buscar_datos(user)

#app
def app():
    
    #estructura
    tabs=estructure()
    
    #modelo de predicciones   
    lable=LinkScribe(tabs)
    
    # Contenido coneccion con base de datos
    #baseDatos(tabs)


if __name__ == '__main__':
    app()