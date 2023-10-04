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

from google.cloud import firestore

API_ENDPOINT = os.environ.get("API_ENDPOINT", "http://localhost:8080")


#prediccion
def call_api_predict_method(link):
    request_data = [{
        "link": link,
                    }]
    
    request_data_json = json.dumps(request_data)
    headers = {
    'Content-Type': 'application/json'
                }
    print(request_data_json)
    predict_method_endpoint = f"{API_ENDPOINT}/scrapper/predict"
    response = requests.request("POST",predict_method_endpoint , headers=headers, data=request_data_json)
    response_json = response.json()
    predictions = response_json['detail']
    label = predictions
    return label

#estructura inicial de la app
def estructure():
    
    st.set_page_config(page_title="Andrea App",page_icon="🧊")
    
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

        #verificamos que sea un link correcto
        if submit_button:
            if link:
                
                label=call_api_predict_method(link)
                #label=1
                # Cuadro de Información del Enlace
                st.subheader("Título de la pagina:")
                st.write(link)
                st.subheader("Descripción:")
                st.write(link)  
                st.subheader("imagen de vista previa:")
                st.write(link)           
                st.subheader("LINK:")
                st.write(link) 
                st.subheader("Categoria:",)  

            # Aquí puedes agregar la lógica para procesar el enlace después de hacer clic en el botón
            else:
                # Mensaje de error  ingresó una URL
                st.markdown("<p style='color: red;'>Por favor, ingresa una URL.</p>", unsafe_allow_html=True)
    return(label)

#comunicacion con la base de datos
def baseDatos(tabs):
     with tabs[1]:
    # Aquí puedes agregar la lógica y código para mostrar gráficas
        st.title("BASE DE DATOS")

        #setting up the database
        # Authenticate to Firestore with the JSON account key.
        db = firestore.Client.from_service_account_json("firestore-key.json")

        # Create a reference to the Google post.
        doc_ref = db.collection("users").document("Google")

        # Then get the data at that reference.
        doc = doc_ref.get()

        # Let's see what we got!
        st.write("The id is: ", doc.id)
        st.write("The contents are: ", doc.to_dict())

        # This time, we're creating a NEW post reference for Apple
        doc_ref2 = db.collection("users").document("andrea")

        # Then get the data at that reference.
        doc2 = doc_ref2.get()

        # And then uploading some data to that reference

        dato2 = {"category":"education",
                      "description":"holi",
                      "image":"newimg",
                      "title":"salut"
         }
        doc_ref2.set({
            "dato2": dato2})
        
        # Let's see what we got!
        st.write("The id is: ", doc2.id)
        st.write("The contents are: ", doc2.to_dict())

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