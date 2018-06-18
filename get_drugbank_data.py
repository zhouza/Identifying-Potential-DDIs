import json
import xmltodict
from pymongo import MongoClient
import os
import sys
import pandas as pd

def convert_xml_to_dict(xml_file, xml_attribs=True):
    ''' takes xml filepath input and returns dict
    '''
    with open(xml_file, "rb") as f:
        d = xmltodict.parse(f, xml_attribs=xml_attribs)
        return d

client = MongoClient('mongodb://xx:xx@xx/drugbank')
db = client.drugbank
drugs = db.drugs

print('connected to mongo')

d = convert_xml_to_dict('data/full database.xml')

print('conversion complete')

drugs.insert_many(d['drugbank']['drug'])

print('records inserted into mongo') 

