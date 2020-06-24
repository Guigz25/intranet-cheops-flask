import json
from collections import OrderedDict

def load_db():
    with open("db.json") as data_file:
        return json.load(data_file)

def save_db():
    with open("db.json", "w") as f:
        return json.dump(db, f, sort_keys=True)

def get_index(nom, prenom):
    db = load_db()
    y=0
    for i in db: 
        # print(i['Nom'])
        if i['Nom'] == nom :
            if i['Prenom'] == prenom:
                return y
        
        y += 1


# path =  "/var/www/intranet-cheops-flask/db.json"
db = load_db()
