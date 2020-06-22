from flask import Flask, render_template, request, url_for, redirect, jsonify
from model import db, save_db, load_db, get_index
import random


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():  
    if request.method == "POST":
        if request.form['nom'] and request.form['prenom'] and request.form['equipe'] != "Choisir l'équipe parmie la liste":
            nom = request.form['nom']
            prenom = request.form['prenom']
            equipe = request.form['equipe']
            response = request.get_data()

            personne_select = {
                "Nom" : nom,
                "Prenom": prenom,
                "Equipe": equipe
            }
            if request.form['type'] == 'update':
                index=int(request.form['index'])
                if db[index]['Nom'] == request.form['nom'] and db[index]['Prenom'] == request.form['prenom'] and db[index]['Equipe'] == request.form['equipe'] :
                    print("error")
                    return jsonify({'error': 'Veuillez modifier au moins un champ'})
                else:
                    db[index]['Nom'] = request.form['nom']
                    db[index]['Prenom'] = request.form['prenom']
                    db[index]['Equipe'] = request.form['equipe']
                    save_db()
                    nomPrenom = personne_select['Nom'] + " " + personne_select['Prenom']
                    return_value = {
                    'nomPrenom': nomPrenom
                    }
                    return return_value
                    

            elif request.form['type'] == 'suppression':
                # index = get_index(request.form['nom'], request.form['prenom'])
                index=int(request.form['index'])
                db.pop(int(index))
                save_db()
                return_value = {
                    'index': index
                }
                return return_value

            elif request.form['type'] == 'ajout' :
                db.append(personne_select)
                save_db()

                nomPrenom = personne_select['Nom'] + " " + personne_select['Prenom']
                return_value = {
                    'nomPrenom': nomPrenom
                }
            
                return return_value
        else:
            print("error")
            return jsonify({'error': 'Veuillez remplir tous les champs'})
    else:
        return render_template("member.html", personnes=db)



@app.route("/gagnant", methods=["GET", "POST"])
def gagnant():  
    if request.method == "POST":
        if request.form['type'] == 'gagnant':
            print("gagnant")
            random.shuffle(db)
            gagnants = {
                'gagnant': db[0]['Nom'] + " " + db[0]['Prenom'],
                'backup': db[1]['Nom'] + " " + db[1]['Prenom'],                 
            }
            return gagnants
        else:
            print('error')
            return jsonify({'error': 'Désolé, il y a eu un problème lors de l\'execution du script ... Veuillez contacter l\'administrateur'})

