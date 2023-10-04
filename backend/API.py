from load_model import model_load
from fastapi import FastAPI
from scrapper_controller import router as scrapper_router
from fastapi import Depends, Request
from translate import Traductor
from scrapper import Scrapper


app = FastAPI()


async def get_model(request:Request):
    return request.app.state.model

async def get_traductor(request:Request):
    return request.app.state.traductor

async def get_scrapper(request:Request):
    return request.app.state.scrapper




@app.on_event("startup")
def load_model():
    #this function will run once when the application starts up
    print("Loading the model...")
   
    model = model_load()
    print("Model loaded successfully!")
    app.state.model = model
    
@app.on_event("startup")
def load_traductor():
    traductor=Traductor()
    app.state.traductor = traductor
    
@app.on_event("startup")    
def load_scrapper():
    scrapper=Scrapper()
    app.state.scrapper= scrapper
    




@app.on_event("shutdown")
def shutdown_event():
    """this function will run once when the application shuts down"""
    print("Shutting down the application...")
  



app.include_router(
    scrapper_router, 
    tags=["scrapper"],
    prefix="/scrapper"
)

@app.get("/hi")
def hi():
    return {"message": "Hello World from the API!!!"}

