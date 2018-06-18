from pymongo import MongoClient
import pandas as pd

def unnest_drug_data(d):
    new_d = {}
    try:
        if type(d['drugbank-id']) != list:
            new_d['drug_id'] = d['drugbank-id']['#text']
        else:
            new_d['drug_id'] = d['drugbank-id'][0]['#text']
        new_d['drug_name'] = d['name']
    except:
        #print(d['_id'], 'no id/name')
        return {}

    try:
        new_d['parent'] = d['classification']['direct-parent']
    except:
        new_d['parent'] = None
    try:
        new_d['kingdom'] = d['classification']['kingdom']
    except:
        new_d['kingdom'] = None
    try:
        new_d['superclass'] = d['classification']['superclass']
    except:
        new_d['superclass'] = None
    try:
        new_d['class'] = d['classification']['class']
    except:
        new_d['class'] = None
    try:
        new_d['subclass'] = d['classification']['subclass']
    except:
        new_d['subclass'] = None

    categories = []

    if d['categories'] == None:
        categories.append(None)
    elif type(d['categories']['category']) != list:
        categories.append(d['categories']['category']['category'])
    else:
        for elem in d['categories']['category']:
            categories.append(elem['category'])
    new_d['category'] = categories

    target_action_ids = []
    target_ids = []
    target_names = []
    target_actions = []

    if d['targets'] == None:
        #print(d['_id'], 'no targets')
        return {}
    # if only one target per drug
    elif type(d['targets']['target']) != list:
        targets = d['targets']['target']
        target_ids = [targets['id']]
        target_names = [targets['name']]
        # if action is null, can't make it part of the id
        if targets['actions'] == None:
            target_action_ids.append(targets['id']+'_'+'None')
            target_actions.append(None)
        # if only one action per target and not null
        elif type(targets['actions']['action']) != list:
            target_action_ids = [targets['id']+'_'+targets['actions']['action']]
            target_actions.append(targets['actions']['action'])
        # if multiple actions per target, iterate
        else:
            # get list of actions
            actions = targets['actions']['action']
            for action in actions:
                target_action_ids.append(targets['id']+'_'+action)
                target_actions.append(action)
    # if multiple targets per drug
    else: 
        targets = d['targets']['target']
        for target in targets:
            target_ids.append(target['id'])
            target_names.append(target['name'])
            if target['actions'] == None:
                target_action_ids.append(target['id']+'_'+'None')
                target_actions.append(None)
            elif type(target['actions']['action']) != list:
                target_action_ids.append(target['id']+'_'+target['actions']['action'])
            # if multiple actions per target, iterate
            else:
                # get list of actions
                actions = target['actions']['action']
                for action in actions:
                    target_action_ids.append(target['id']+'_'+action)
                    target_actions.append(action)

    new_d['target'] = list(zip(target_action_ids,target_ids,target_names,target_actions))

    ddi_ids = []
    ddi_names = []
    ddi_sympts = []
    interactions = d['drug-interactions']
    if interactions == None:
        pass
    elif type(interactions['drug-interaction']) != list:
        ddi_ids.append(interactions['drug-interaction']['drugbank-id'])
        ddi_names.append(interactions['drug-interaction']['name'])
        ddi_sympts.append(interactions['drug-interaction']['description'])
    else:
        for drug in interactions['drug-interaction']:
            ddi_ids.append(drug['drugbank-id'])
            ddi_names.append(drug['name'])
            ddi_sympts.append(drug['description'])

    new_d['ddi'] = list(zip(ddi_ids,ddi_names,ddi_sympts))

    return new_d


client = MongoClient('mongodb://xx:xx@xx/drugbank')
db = client.drugbank
drugs = db.drugs

print('connected to Mongo')

drugs_sub = db.drugs_sub
drugs_sub.insert_many(
    list(drugs.find({},{'_id':0,'drugbank-id':1,
                                    'name':1,'classification':1,
                                    'categories':1,'targets':1,
                                    'drug-interactions':1}))
)

print('subset collection created')

drugs_unnst = db.drugs_unnst

for elem in drugs_sub.find({}):
    drugs_unnst.insert_one(unnest_drug_data(elem))

print('data unnested in Mongo')

