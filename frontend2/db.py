import streamlit as st
from google.cloud import firestore
import random
import string
import json
from google.oauth2 import service_account

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="linkscribe-20b7c")

# Streamlit widgets to let a user create a new post
user = st.text_input("user name")
title = st.text_input("link title")
url = st.text_input("link url")
category = "education"
submit = st.button("Submit new link")

dato = {"category": category,
		"title": title,
		"url": url}
name = ''.join(random.choices(string.ascii_letters, k=10))

# Once the user has submitted, upload it to the database
if user and title and url and submit:
	doc_ref = db.collection("users").document(user)
	doc_ref.set({
		name:dato
	}, merge=True)

# And then render each post, using some light Markdown
user_ref = db.collection("users").document(user)





user_Data = user_ref.get()
user2 = user_Data.to_dict()

st.write(f"**Texto:** {user2}")

posts_ref = db.collection("users")



if user2 is not None:
    # Sidebar para la búsqueda por título
    st.header("Filtrar por Título")
    filtro_titulo = st.text_input("Ingrese el título a buscar:")
    
    # Filtrar datos por título
    datos_filtrados = [dato for dato_id, dato in user2.items() if filtro_titulo.lower() in dato.get("title", "").lower()]

    # Mostrar los datos filtrados
    st.header("Datos Filtrados")

    for item in datos_filtrados:
        if st.button(f"Ver Descripción de '{item['title']}' ({item['url']})"):
            st.subheader("Descripción:")
            st.write(item["url"])
else:
    st.warning("No se encontraron datos para este usuario.")

#post = posts_ref.get()
#post2 = post.to_dict()
#category = post["category"]
#title = post["title"]
#url = post["url"]
#category = post2["dato2"]["category"]

#st.subheader(f"Post: {title}")
#st.write(f":link: [{url}]({url})")
#st.write(f"category: {category}")
#st.write(f"data: {post2} category {category}")
