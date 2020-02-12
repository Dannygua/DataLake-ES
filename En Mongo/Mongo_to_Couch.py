
#script de Python para migrar documentos de mongodb a la base de datos apache couchdb.
#Este script lee un documento de mongodb y lo escribe en la base de datos de couchdb.


import json
from argparse import ArgumentParser
import requests
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


DB_COUNT, DOCUMENT_COUNT = 0, 0
SKIPPED = []
argp = ArgumentParser()
argp.add_argument("-c", "--couchdb", help="couchdb endpoint, example: http://username:password@localhost:5984 ", required=True)
argp.add_argument("-m", "--mongodb", help="mongodb endpoint, example: mongodb://localhost:27017 ", required=True)
args = argp.parse_args()

URL = args.couchdb

# Prueba de conexión CouchDB
try:
    response = requests.get(URL)
    if response.status_code == 200:
        print('CouchDB connection: Success')
    if response.status_code == 401:
        print('CouchDB connection: failed', response.json())
except requests.ConnectionError as e:
    raise e

# encabezados de conexión couchDB
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

CLIENT = MongoClient(args.mongodb)

# Prueba de conexión MongoDB
try:
    CLIENT.admin.command('ismaster')
    print('MongoDB connection: Success')
except ConnectionFailure as cf:
    print('MongoDB connection: failed', cf)


DBS = CLIENT.database_names()  

# leer colecciones y documentos
for db in DBS:
    if db not in ('admin', 'local'): 
        cols = CLIENT[db].collection_names()  
        for col in cols:
            print('Querying documents from collection {} in database {}'.format(col, db))
            for x in CLIENT[db][col].find():  
                try:
                    documents = json.dumps(x)
                except TypeError as t:
                    print('current document raised error: {}'.format(t))
                    SKIPPED.append(x)  
                    continue    
                except Exception as e:
                    raise e
                # crear base de datos en CouchDB por primera vez si no existe
                try:
                    response = requests.Session().get(URL+'/'+db+'-'+col, auth=('admin', 'password'), headers=HEADERS, verify=False)
                    if 'error' in response.json():  # db doesnt exist on destination, create it
                        print('Creating a new database {} in CouchDB'.format(db+'-'+col))
                        output = requests.Session().put(URL+'/'+db+'-'+col, auth=('admin', 'password'), headers=HEADERS, verify=False)
                        if output.status_code == 201 or 202:
                            DB_COUNT += 1
                    # insertar documentos en la base de datos de couchDB.
                    output = requests.Session().post(URL+'/'+db+'-'+col, auth=('admin', 'password'), headers=HEADERS,
                                                     data=documents, verify=False)
                    if output.status_code == 201 or 202:
                        DOCUMENT_COUNT += 1
                except requests.exceptions.RequestException as e:
                    raise e
print('DB migration summary: {} Databases and {} Documents created in CouchDB'.format(DB_COUNT, DOCUMENT_COUNT))
print('Skipped documents: \n {}'.format(SKIPPED))