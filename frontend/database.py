import streamlit as st
from google.cloud import firestore
import random
import string
import json
from google.oauth2 import service_account

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

def guardar_datos(dato,user):

    #creamos un nombre unico
    name = ''.join(random.choices(string.ascii_letters, k=10))

    # Once the user has submitted, upload it to the database
    doc_ref = db.collection("users").document(user)
    doc_ref.set({
            name:dato
                }, merge=True)

def buscar_datos(user):
    
    user_ref = db.collection("users").document(user)

    user_Data = user_ref.get()
    user2 = user_Data.to_dict()

    if user2 is not None:
        # Sidebar para la búsqueda por título
        st.header("Filter by title")
        filtro_titulo = st.text_input("Enter the title to search:")
        
        categorias = ['Adult', 'Business/Corporate', 'Computers and Technology',
       'E-Commerce', 'Education', 'Food', 'Forums', 'Games',
       'Health and Fitness', 'Law and Government', 'News', 'Photography',
       'Social Networking and Messaging', 'Sports', 'Streaming Services',
       'Travel']

        # Sidebar para la búsqueda por categoría
        st.header("Filter by category")
        filtro_categoria = st.multiselect("Select category", categorias)

        # Filtrar datos por título y categoría
        datos_filtrados = [
            dato for dato_id, dato in user2.items() 
            if filtro_titulo.lower() in dato.get("titulo", "").lower() 
            and (not filtro_categoria or dato.get("categoria", "") in filtro_categoria)
        ]


        if datos_filtrados:
            # Mostrar los datos filtrados
            st.header("Filtered data")
            for item in datos_filtrados:
                if st.button(f"Show description of {item['titulo']}, of the category: {item['categoria']} "):
                    st.subheader("Title:")
                    st.write(item['titulo'])
                    st.subheader("Category:")
                    st.write(item['categoria'])
                    st.subheader("Image:")
                    st.image(item['imagen'])
                    st.subheader("Description:")
                    st.write(item["descripcion"])
                    st.subheader("LINK:")
                    st.write(item['link'])
                    
            
        else:    
            st.warning("No se encontraron datos para este usuario.")
        
        
    else:
        st.warning("No se encontraron datos para este usuario.")

import os
import firebase_admin
from firebase_admin import credentials

import functools

def run_once(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            func(*args, **kwargs)
            wrapper.has_run = True
    wrapper.has_run = False
    return wrapper

@run_once
def funcion_a_ejecutar():
    cred = credentials.Certificate("firestore-key.json")
    firebase_admin.initialize_app(cred)
    print("Esta función se ejecutará solo una vez.")
