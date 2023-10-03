from load_model import model_load
#from translate import Traductor
#from scrapper import scrapper
from fastapi import FastAPI
'''

URL = "https://spartangeek.com/blog/cu%C3%A1nto-cuesta-una-pc-gamer-en-m%C3%A9xico"
scrapper=scrapper()
article=scrapper.read_url(URL)
chunks=scrapper.text_processor(article)
resume=scrapper.summarize(chunks)
print(resume)

traductor = Traductor()
texto = traductor.Traducir(resume)

prediction=model.predict([texto])
print(prediction)
'''

app = FastAPI()

@app.on_event("startup")
def load_model():
    #this function will run once when the application starts up
    print("Loading the model...")
   
    model = model_load()
    print("Model loaded successfully!")
    app.state.model = model



@app.on_event("shutdown")
def shutdown_event():
    """this function will run once when the application shuts down"""
    print("Shutting down the application...")
  

app.include_router(
    users_router, 
    tags=["users"], 
    prefix="/users"
)

app.include_router(
    iris_router, 
    tags=["iris"],
    prefix="/iris"
)

@app.get("/hi")
def hi():
    return {"message": "Hello World from the API!!!"}

