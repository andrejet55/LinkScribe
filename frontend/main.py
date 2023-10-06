import streamlit as st
from streamlit_option_menu import option_menu
import easylink

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        easylink.app()          
             
    run()            
         
