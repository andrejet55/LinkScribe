from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from load_model import model_load
from scrapper import Scrapper       
from translate import Traductor
from fastapi import Request, Depends
import typing
import numpy as np
from typing import List



class URLItem(BaseModel):
    link: str

router = InferringRouter()

async def get_model(request:Request):
    return request.app.state.model


async def get_traductor(request:Request):
    return request.app.state.traductor

async def get_scrapper(request:Request):
    return request.app.state.scrapper

@cbv(router)


class scrapper_controller:
    
    model: model_load = Depends(get_model)
    traductor: Traductor =Depends(get_traductor)
    scrapper: Scrapper =Depends(get_scrapper)
    
    @router.post("/predict")
    
    def predict(self,URLS:List[URLItem]):
        #URL= np.array([URL.to_numpy() for URL in URLS])
        URLS = URLS[0].link
        print(URLS)
        #URL=list(URL[0].values())
        #URL=str(URL[0])
        
        article=self.scrapper.read_url(URLS)
        chunks=self.scrapper.text_processor(article)
        resume=self.scrapper.summarize(chunks)
        
        texto = self.traductor.Traducir(resume)
        
        prediction=self.model.predict([texto])
        
        titulo=self.scrapper.obtener_titulo(URLS)
        img=self.scrapper.obtener_imagen(URLS)
        
        return prediction,texto,titulo,img
    
    
    





