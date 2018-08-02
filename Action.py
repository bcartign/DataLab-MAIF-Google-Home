# MAIF DataLab Bruno CARTIGNY
# 02.08.18 - ajout API v2

# -*- coding: utf-8 -*-

import Utilitaire as util
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

DEBUG = True


class ActionV2():
    """
        Classe pour traiter les actions des intents venant de DialogFlow v2
            Quiz - nouvelle question
            Quiz- vérifier réponse
            Annuaire
    """

    def testContext(**kwargs):
        requete = kwargs['request']
        sessionID = kwargs['session']
        if DEBUG:
            print("DEBUG : testContext call debugAllContextV2")
            util.debugAllContextV2(requete, sessionID)
        return True

    def verifierReponse(**kwargs):
        if DEBUG:
            if DEBUG:
                print("DEBUG : Action : verifierReponse")
        parameters = kwargs['request']
        # sessionID = kwargs['session']
        lstQuestion = parameters['queryResult'][
            'outputContexts'][0]['parameters']['lstQuestionPose']

        # Bonne réponse
        if(parameters['queryResult']['parameters']['reponse'].strip() != ""):
            return {"repondu": True, "nouvelleQuestion": util.selectQuestion(lstQuestionRep=lstQuestion)}
        else:
            return {"repondu": False}

    def selectQuiz(**kwargs):
        if DEBUG:
            if DEBUG:
                print("DEBUG : Action : selectQuiz")
        parameters = kwargs['request']
        sessionID = kwargs['session']

        util.NB_QUESTION = int(util.getContextV2(
            parameters, "C_QUIZ", session=sessionID).get('nbQuestion'))

        if 'lstQuestionPose' in parameters['queryResult']['outputContexts'][0]['parameters']:
            lstQuestion = parameters['queryResult'][
                'outputContexts'][0]['parameters']['lstQuestionPose']

            if(len(lstQuestion) == util.NB_QUESTION):
                lstQuestion = []

            return {"nouvelleQuestion": util.selectQuestion(lstQuestionRep=lstQuestion)}

        return util.selectQuestion(lstQuestionRep=[])

    def retourtransfert(**kwargs):
        requete = kwargs['request']
        sessionID = kwargs['session']
        if DEBUG:
            print("DEBUG : Action.retourtransfert start calling debugAllContextV2")
            util.debugAllContextV2(requete, sessionID)     
        leContext1 = util.getContextV2(requete, 'c_ldap', session=sessionID)
        leContext2 = util.getContextV2(requete, 'c_temp', session=sessionID)
        return [leContext1, leContext2]

    def getInformationAnnuaire(**kwargs):
        sessionID = kwargs['session']
        requete = kwargs['request']
        listUsers = kwargs['listUser']
        listNoms = kwargs['listNom']
        if DEBUG:
            print("DEBUG : Action.getInformationAnnuaire")
            util.debugAllContextV2(requete, sessionID)

        leContext_LDAP = util.getContextV2(
            requete, 'c_ldap', session=sessionID)
        leContext_LDAP_REPONSE = util.getContextV2(
            requete, 'c_ldap_reponse', session=sessionID)
        leContext_LDAP_TEMP = util.getContextV2(
            requete, 'c_ldap_temp', session=sessionID)

        nom = leContext_LDAP.get('nom')
        prenom = leContext_LDAP.get('prenom')
        telephone = leContext_LDAP.get('telephone')
        autre = leContext_LDAP.get('autre')
        # batiment = ''

        # Ce cas ce produit si la personne n'a renseigné qu un prénom
        # ou le nom correspond à plusieurs prénoms
        if (nom.strip() == "" and not autre):
            if DEBUG:
                print("DEBUG : 1-nom.strip()=" +
                      nom.strip() + " autre=" + autre)
            if leContext_LDAP_TEMP is not None:
                nom = leContext_LDAP_TEMP.get('nomTemp')

        if (leContext_LDAP_REPONSE is not None):
            if not nom or nom == leContext_LDAP.get('prenom'):
                nom = leContext_LDAP_REPONSE.get('nom.original')
                prenom = leContext_LDAP_REPONSE.get('prenom')
                if DEBUG:
                    print("DEBUG : 2-nom2=" + nom + " prenom2=" + prenom)

        if(prenom and autre and not nom):
            if DEBUG:
                print("DEBUG : 6-prenom=" + prenom + " autre=" + autre)
            fu = []
            # Fuzzy_Search de la librairie fuzzywuzzy
            # fu = process.extract(autre, listUsers, limit=1)
            fu, ratio = process.extractOne(autre, listNoms, scorer=fuzz.ratio)
            if DEBUG:
                print("DEBUG : probable=" + str(fu) + " ; ratio=" + str(ratio))
            nom = fu
            # return nom

        if(telephone):
            if DEBUG:
                print("DEBUG : 3-telephone=" + telephone)
            for u in listUsers:
                # if DEBUG : print("DEBUG : for u in Listusers")
                if util.formatTelephone(u.telephone) == util.formatTelephone(telephone):
                    return u

        if(nom and not prenom):
            if DEBUG:
                print("DEBUG : 4-nom seul=" + nom)
            tempListUsers = []
            for u in listUsers:
                if u.nom.lower() == nom.lower():
                    tempListUsers.append(u)

            if len(tempListUsers) == 1:
                return tempListUsers[0]

            if DEBUG:
                print("DEBUG : 4-tempListUsers=" + str(tempListUsers))
            return tempListUsers

        if(prenom and nom):
            if DEBUG:
                print("DEBUG : 5-nom=" + nom + " prenom=" + prenom)
            for u in listUsers:
                if u.nom.lower() == nom.lower() and u.prenom.lower() == prenom.lower():
                    return u

        return None


class Action():
    """
        Classe permettant de traiter les actions des intents venant de DialogFlow v1
            Quiz - nouvelle question
            Quiz- vérifier réponse
            Annuaire
    """

    def verifierReponse(**kwargs):
        parameters = kwargs['request']
        lstQuestion = parameters['result']['contexts'][
            0]['parameters']['lstQuestionPose']

        # Bonne réponse
        if(parameters['result']['parameters']['reponse'].strip() != ""):
            return {"repondu": True, "nouvelleQuestion": util.selectQuestion(lstQuestionRep=lstQuestion)}
        else:
            return {"repondu": False}

    def selectQuiz(**kwargs):
        parameters = kwargs['request']

        util.NB_QUESTION = int(util.getContext(
            parameters, "C_QUIZ").get('nbQuestion'))

        if 'lstQuestionPose' in parameters['result']['contexts'][0]['parameters']:
            lstQuestion = parameters['result']['contexts'][
                0]['parameters']['lstQuestionPose']

            if(len(lstQuestion) == util.NB_QUESTION):
                lstQuestion = []

            return {"nouvelleQuestion": util.selectQuestion(lstQuestionRep=lstQuestion)}

        return util.selectQuestion(lstQuestionRep=[])

    def transfert(**kwargs):
        requete = kwargs['request']
        leContext1 = util.getContext(requete, 'c_ldap')
        leContext2 = util.getContext(requete, 'c_temp')
        return [leContext1, leContext2]

    def getInformationAnnuaire(**kwargs):

        requete = kwargs['request']
        listUsers = kwargs['listUser']
        listNoms = kwargs['listNom']

        leContext_LDAP = util.getContext(requete, 'c_ldap')
        leContext_LDAP_REPONSE = util.getContext(requete, 'c_ldap_reponse')
        leContext_LDAP_TEMP = util.getContext(requete, 'c_ldap_temp')

        nom = leContext_LDAP.get('nom')
        prenom = leContext_LDAP.get('prenom')
        telephone = leContext_LDAP.get('telephone')
        autre = leContext_LDAP.get('autre')
        # batiment = ''

        # Ce cas ce produit si la personne n'a renseigné qu un prénom
        # ou le nom correspond à plusieurs prénoms
        if (nom.strip() == "" and not autre):
            if DEBUG:
                print("DEBUG : 1-nom.strip()=" +
                      nom.strip() + " autre=" + autre)
            if leContext_LDAP_TEMP is not None:
                nom = leContext_LDAP_TEMP.get('nomTemp')

        if (leContext_LDAP_REPONSE is not None):
            if not nom or nom == leContext_LDAP.get('prenom'):
                nom = leContext_LDAP_REPONSE.get('nom.original')
                prenom = leContext_LDAP_REPONSE.get('prenom')
                if DEBUG:
                    print("DEBUG : 2-nom2=" + nom + " prenom2=" + prenom)

        if(prenom and autre and not nom):
            if DEBUG:
                print("DEBUG : 6-prenom=" + prenom + " autre=" + autre)
            fu = []
            # Fuzzy_Search de la librairie fuzzywuzzy
            # fu = process.extract(autre, listUsers, limit=1)
            fu, ratio = process.extractOne(autre, listNoms, scorer=fuzz.ratio)
            if DEBUG:
                print("DEBUG : probable=" + str(fu) + " ; ratio=" + str(ratio))
            nom = fu
            # return nom

        if(telephone):
            if DEBUG:
                print("DEBUG : 3-telephone=" + telephone)
            for u in listUsers:
                # if DEBUG : print("DEBUG : for u in Listusers")
                if util.formatTelephone(u.telephone) == util.formatTelephone(telephone):
                    return u

        if(nom and not prenom):
            if DEBUG:
                print("DEBUG : 4-nom seul=" + nom)
            tempListUsers = []
            for u in listUsers:
                if u.nom.lower() == nom.lower():
                    tempListUsers.append(u)

            if len(tempListUsers) == 1:
                return tempListUsers[0]

            if DEBUG:
                print("DEBUG : 4-tempListUsers=" + str(tempListUsers))
            return tempListUsers

        if(prenom and nom):
            if DEBUG:
                print("DEBUG : 5-nom=" + nom + " prenom=" + prenom)
            for u in listUsers:
                if u.nom.lower() == nom.lower() and u.prenom.lower() == prenom.lower():
                    return u

        return None
