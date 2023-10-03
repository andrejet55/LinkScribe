from deep_translator import GoogleTranslator

class Traductor():
    
    def __init__(self, target='en',source='auto'):
        
        self.target ='en'
        self.source ='auto'
    
    def Traducir(self,data):
        
       
        translator = GoogleTranslator(source='auto', target='en')
        translated=translator.translate(data)
        return translated
    
