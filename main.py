# MAIF DataLab Bruno CARTIGNY
# 02.08.18 - ajout API v2

# -*- coding: utf-8 -*-

import json
import csv
import os
from Action import Action, ActionV2
from User import User
from Message import Message, MessageV2

from flask import Flask, request, make_response

DEBUG = True
FICHIER_UTILISATEUR = 'annuaire.csv'

app = Flask(__name__)
listUsers = []
listNoms = []


@app.route('/')
def hello():
    return "Le serveur DataLab MAIF (Heroku) est à l'écoute..."


@app.route('/dialog', methods=['POST'])
def dialog():

    req = request.get_json(silent=True, force=True)
    if DEBUG:
        print('=========== main ===========')
    texte = req["queryResult"]
    action = req["queryResult"]["action"]
    sessionID = req["session"]
    message = {}
    if DEBUG:
        print('DEBUG : texte=', texte, ' action=', action)
    if sessionID:
        if action:
            res = getattr(ActionV2, action)(
                request=req, listUser=listUsers, listNom=listNoms, session=sessionID)
            message = getattr(MessageV2, "{0}_message".format(action))(
                reponse=res, request=req, session=sessionID)

    if DEBUG:
        print('DEBUG : message=', json.dumps(message))
    r = make_response(json.dumps(message))
    r.headers['Content-Type'] = 'application/json; charset=utf-8'
    if DEBUG:
        print('=========== end main ===========')
    return r


@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    action = req['result']['action']
    message = {}

    if action:
        res = getattr(Action, action)(
            request=req, listUser=listUsers, listNom=listNoms)
        message = getattr(Message, "{0}_message".format(action))(
            reponse=res, request=req)

    r = make_response(json.dumps(message))
    r.headers['Content-Type'] = 'application/json; charset=utf-8'
    return r


def loadUser(listUsers, listNoms):
    with open(FICHIER_UTILISATEUR, "r") as csvfile:
        datas = csv.reader(csvfile, delimiter=';')
        for row in datas:
            # if(len(row[2]) > 5):
            #    row[2] = '0' + row[2]
            listUsers.append(User(row[0], row[1], row[2], row[3]))
            listNoms.append(row[0])


if __name__ == 'main':

    print('Chargement des utilisateurs ...')
    loadUser(listUsers, listNoms)
    print('Chargement des utilisateurs nb:{0} - OK'.format(len(listUsers)))


if __name__ == '__main__':

    if DEBUG:
        print('DEBUG : Chargement des utilisateurs ...')
    loadUser(listUsers, listNoms)
    print('Chargement des utilisateurs nb:{0} - OK'.format(len(listUsers)))

    print('Démarrage du serveur ')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)
