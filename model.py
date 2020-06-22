import json


def load_db():
    with open("db.json") as f:
        return json.load(f)


def save_db():
    with open("db.json", "w") as f:
        return json.dump(db, f)

def get_index(nom, prenom):
    db = load_db()
    y=0
    for i in db: 
        # print(i['Nom'])
        if i['Nom'] == nom :
            if i['Prenom'] == prenom:
                return y
        
        y += 1


        
db = load_db()
