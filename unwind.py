from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb://xx:xx@xx/drugbank')
db = client.drugbank
drugs = db.drugs

drugs_unnst = db.drugs_unnst
drugs_targets = db.drugs_targets
targets = db.targets
drugs_int = db.drugs_int

print('connected to Mongo')

drugs_unnst.aggregate([{'$project':{'_id':0,'ddi':0}},
                                 {'$unwind':'$category'},
                                 {'$unwind':'$target'},
				 {'$out':'drugs_targets'}
                             ])

print('targets unwound and new collection created')

drugs_unnst.aggregate([{'$project':{'_id':0,'category':0,'target':0}},
                                 {'$unwind':'$ddi'},
				 {'$out':'drugs_int'}
                             ])

print('ddi unwound and new collection created')
