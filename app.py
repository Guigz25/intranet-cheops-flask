from flask import Flask, render_template, request, url_for, redirect, jsonify
from model import db, save_db, load_db, get_index
import random
from hp3parclient import client, exceptions
import pprint




app = Flask(__name__)
app.debug = True

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
                nomPrenom = personne_select['Nom'] + " " + personne_select['Prenom']
                return_value = {
                    'index': index,
                    'nomPrenom': nomPrenom

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



@app.route("/wwn")
def wwn():
    ip_address = '192.168.92.101'
    username = '3paradm'
    password = 'Arr@y_3R'

    cl = client.HP3ParClient("https://%s:8080/api/v1" % ip_address, suppress_ssl_warnings=True)
    cl.setSSHOptions(ip_address, username, password)

    try : 
        cl.login(username, password)

        port = cl.getFCPorts()
        volumes = cl.getVolumes()

        luns = []
        lun = {}
        # On parcourt le nombre total de lun et on ressort le nom de la lun
        for i in range(int(volumes['total'])):
            # print(volumes['members'][i]['name'])
            # luns.append(volumes['members'][i]['name'])

            lun = { 
                'nom': volumes['members'][i]['name'],
                'taille': int(int(volumes['members'][i]['sizeMiB']) / 1024)
            }
            luns.append(lun)

    except exceptions.HTTPUnauthorized as ex:
       pprint.pprint("You must login first")
    except Exception as ex:
       print(ex)

    print(luns)


    cl.logout()
    print("logout worked")

    # print(volumes)

    lun = volumes['members'][74]['name']
    return render_template('wwn.html', luns=luns)