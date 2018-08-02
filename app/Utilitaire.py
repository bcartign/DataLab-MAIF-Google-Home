# MAIF DataLab Bruno CARTIGNY
# 02.08.18 - ajout API v2

# -*- coding: utf-8 -*-

from random import randint

DEBUG = True
NB_QUESTION = 8


def selectQuestion(**kwargs):
    lstQuestionRep = kwargs['lstQuestionRep']

    if len(lstQuestionRep) == NB_QUESTION:
        return -1

    laQuestion = randint(1, NB_QUESTION)
    while laQuestion in lstQuestionRep:
        laQuestion = randint(1, NB_QUESTION)

    lstQuestionRep.append(laQuestion)
    return laQuestion


def getContextV2(requete, nom, session):
    lstContext = requete['queryResult']['outputContexts']
    sessionID = session
    for c in lstContext:
        if c['name'].lower() == sessionID + "/contexts/" + nom.lower():
            return c['parameters']
    return None


def debugAllContextV2(requete, session):
    lstContext = requete['queryResult']['outputContexts']
    sessionID = session
    for ctxt in ('c_ldap', 'c_temp', 'c_ldap_reponse', 'c_ldap_temp'):
        for c in lstContext:
            if c['name'].lower() == sessionID + "/contexts/" + ctxt:
                print("DEBUG: util.debugAllContextV2 resultat: contexte=",
                      ctxt, " parametres= ", c)
    return None


def getContext(requete, nom):
    lstContext = requete['result']['contexts']

    for c in lstContext:
        if c['name'].lower() == nom.lower():
            return c['parameters']
    return None


def getCibleV2(context):
    if DEBUG:
        print("DEBUG : util.getCibleV2 pour contexte=", context)
    res = (context.get('intentOrigine').split('_'))[-1].upper()
    return "E_LDAP_REPONSE_{0}".format(res)


def getCible(context):
    res = (context.get('intentOrigine').split('_'))[-1].upper()
    return "E_LDAP_REPONSE_{0}".format(res)


def formatTelephone(number):
    # print(number)
    if(number != "inconnu"):
        if(len(number) > 6):
            if(number[0] != "0"):
                number = "0" + number

            if(number[2] != " "):
                number = " ".join(number[i:i + 2]
                                  for i in range(0, len(number), 2))
    return number
