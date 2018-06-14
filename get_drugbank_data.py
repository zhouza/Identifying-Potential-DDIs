import json
import xmltodict
from pymongo import MongoClient
import subprocess

def convert_xml_to_json(xml_file, xml_attribs=True, store_output = False, output_path = ''):
    ''' takes xml filepath input and returns dict
        if store_output is True and output filepath is provided, saves to filepath provided
    '''
    with open(xml_file, "rb") as f:
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        output = json.dumps(d, indent=4)
        if (store_output == True) and (output_path != ''):
            output_file = open(output_path,'w')
            output_file.write(output)
        return output

def start_mongo_database(database_name, path_to_database):
    mongod = subprocess.run(["", "-l"]) 
        "mongod --dbpath {0}".format(path_to_database),
        shell=True
    )
    client = MongoClient()
    db = client[database_name]
    collection = db['test_collection']
    collection.insert_one({'something new':'some data'})
    mongod.terminate()


from pymongo import MongoClient
client = MongoClient()
db = client.drugbank
drugs = db.drugs
drugs.insert_many(d['drugbank']['drug'])