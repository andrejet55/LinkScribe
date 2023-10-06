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
import database 
from google.cloud import firestore
#LOGIN
import streamlit as st
from firebase_admin import firestore
from firebase_admin import auth
from fastapi import FastAPI, Request


#Connection to port 8080
API_ENDPOINT = os.environ.get("API_ENDPOINT", "http://localhost:8080")

#Creates a new variable to hold the results of the model
if 'dic' not in st.session_state:
    st.session_state.dic = {}

#website title
st.set_page_config(page_title="LinkScribe (◉‿◉)")

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

#initialize FASTAPI
app = FastAPI()
database.funcion_a_ejecutar()

#prediction
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

#set parameters to return to login screen
def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

#App's primary structure
def estructure():
        
    # App title
    st.markdown("<h1 style='text-align: center;'>LinkScribe</h1>", unsafe_allow_html=True)
    st.sidebar.image("andrea.gif")
    
    
        # Model info
    with st.sidebar:
        selected = option_menu(
        menu_title = "Model setting",
        options = ["Model"],
        icons = ["book"],
        menu_icon = "cloud",
        default_index = 0,)

    # Model code
    if selected=="Model":
        
        st.sidebar.subheader("Model description")
        #description of the model
        st.sidebar.write("Use of transformers and SVC to classify the link in base of its metadata obtained through web scrapping")
        st.sidebar.write('NAME: ',st.session_state.username)
        st.sidebar.write('EMAIL: ',st.session_state.useremail)
        st.sidebar.button('Sign out', on_click=t) 
     # Create tabs
    tabs = st.tabs(["APP", "LIBRARY",])

    return(tabs)

#clasiffication using the model
def LinkScribe(tabs,user):
    label=[]
    #"APP" tab content
    with tabs[0]:
        
        # Subpage content
        st.markdown("<h1 style='text-align:;'>EasyLink</h1>", unsafe_allow_html=True)
        
        # Link input
        link = st.text_input("Paste the link:", "")
        submit_button = st.button("Process link")

        #Check the link input
        if submit_button:
            if link:
                      
                label=call_api_predict_method(link)
                
                st.subheader("Category:",)
                st.write(str(label[0]).upper()) 
                
                values = list(label)
                st.subheader("website title:")
                st.write(str(label[2][0]).upper()) 

                st.subheader("Description:")
                st.write(str(label[1]))
                
                st.subheader("LINK:")
                st.write(link) 
                
                st.subheader("Image preview:")
                st.write("")
                st.image(label[3], caption="Image caption")
                
                #Dictionary containing the data results from the model
                mi_diccionario = {
                                'categoria': label[0],
                                'descripcion': label[1],
                                'titulo':label[2][0],
                                'imagen':label[3],
                                'link':link
                                }
                
                #Holds the results info
                st.session_state.dic = mi_diccionario

                #Save the results in the database for the current user session
                database.guardar_datos(st.session_state.dic,user)
                st.balloons()
            else:
                # Mensaje de error  ingresó una URL
                st.markdown("<p style='color: red;'>Please enter an URL</p>", unsafe_allow_html=True)

#Communication with the database to fetch for data
def baseDatos(tabs,user):
     with tabs[1]:
        database.buscar_datos(user)

def app():

    #Check if there is a username and email for this session
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    #Logs in, holds the username and email and set the state as signed in
    def f(): 
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            
            global Usernm
            Usernm=(user.uid)
            
            st.session_state.signedout = True
            st.session_state.signout = True    
	        
        except: 
            st.warning('Login Failed')

    #Initialize the signedout variables
    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
        
    #If there is no user signed in, ask for the login info
    if  not st.session_state["signedout"]: # only show if the state is False, hence the button has never been clicked
        st.title('Welcome to :orange[LinkScribe] :globe_with_meridians:')
        
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password',type='password')
        
        #Sign up 
        if choice == 'Sign up':
            username = st.text_input("Enter  your unique username")
            user_id = username
            if st.button('Create my account'):
                user = auth.create_user(email = email, password = password,uid=username)
                
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()

        else:
            # Login button, calls the main screen       
            st.button('Login', on_click=f)
            
            
    if st.session_state.signout:
                
                #estructura
                tabs=estructure()
                
                #modelo de predicciones   
                LinkScribe(tabs,st.session_state.username)
                
                # Contenido coneccion con base de datos
                baseDatos(tabs,st.session_state.username)
                
                
if __name__ == '__main__':
    app()