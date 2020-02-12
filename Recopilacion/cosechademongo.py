import pymongo #Libreria de MongoDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON
from pymongo import MongoClient

###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "HvCg23VwyIGwnVe5krvHKuZGO"
csecret = "KUwAEDDqogw0xlHr1LQiaECD4q42gpFRPkUS0NLHZm51Y9gMRF"
atoken = "115946548-x5JL2LFNp26y2t0WlBvQE7GirkGeNZUaYLUM1GGL"
asecret = "ul2Q4nw9112ATj4iyFu2VIj12IElGb0GRIr3wBnBPxBAE"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.collection.insert_one(dictTweet) #Aqui se guarda el tweet en la base de mongoDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#Setear la URL del servidor de MongoDB 
client = pymongo.MongoClient("mongodb+srv://pablo:12345@cluster0-ok93s.mongodb.net/test?retryWrites=true&w=majority") 
db = client.basePeru #Test será el nombre de la base de datos donde se almacenarán los tweets
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(track=["ecuador","ineficiencia", "ineptos","renunciaromo","yunda","corrupcion", "correa", "glass", "paronacional"])
twitterStream.filter(locations=[0.22985,-78.5249481,2.1961601,-79.8862076])

