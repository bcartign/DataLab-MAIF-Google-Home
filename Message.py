# MAIF DataLab Bruno CARTIGNY
# 03.08.18 - ajout API v2


# -*- coding: utf-8 -*-

from User import User
import Utilitaire as util

DEBUG = True


class MessageV2():
    """
        Classe permettant de retourner un message à DialogFlow API v2
            Quiz - nouvelle question
            Quiz- vérifier réponse
            Annuaire - demande de précision
            Annuaire - réponse
    """

    def testContext_message(**kwargs):
        if DEBUG:
            print("DEBUG : testContext_message")
        sessionID = kwargs['session']
        request = kwargs['request']
        return {
            "outputContexts": [
                {
                    "name": sessionID + "/contexts/c_ldap_temp",
                    "lifespanCount": 15,
                    "parameters": {
                        "intentOrigine": request['queryResult']['intent']['displayName']
                    }
                }
            ],
            "source": "webhook",
            "followupEventInput": {
                "name": "AnnuaireFin",
                "languageCode": "fr-fr"
            }
        }

    def verifierReponse_message(**kwargs):
        if DEBUG:
            print("DEBUG : verifierReponse_message")
        reponse = kwargs['reponse']
        request = kwargs['request']
        sessionID = kwargs['session']

        lstQuestion = request['queryResult']['outputContexts'][
            0]['parameters']['lstQuestionPose']

        derniereQuestion = 0

        if reponse.get('nouvelleQuestion') == -1:
            derniereQuestion = int(lstQuestion[-1])
        if len(lstQuestion) > 1:
            derniereQuestion = int(lstQuestion[-2])

        if not reponse['repondu']:
            return {
                "followupEventInput": {
                    "name": "E_INFORMATION_QUESTION_{0}".format(int(lstQuestion[-1])),
                    "languageCode": "fr-fr"
                }
            }

        if (reponse['nouvelleQuestion'] == -1):
            return {
                "outputContexts": [
                    {
                        "name": sessionID + "/contexts/c_question{0}".format(derniereQuestion),
                        "lifespanCount": 0
                    },
                    {
                        "name": "c_param_quiz",
                        "lifespanCount": 0
                    }
                ],
                "followupEventInput": {
                    "name": "E_QUIZ_TERMINE",
                    "languageCode": "fr-fr"
                }
            }

        return {
            "outputContexts": [
                {
                    "name": sessionID + "/contexts/c_question{0}".format(derniereQuestion),
                    "lifespanCount": 0,
                    "parameters": {}
                },
                {
                    "name": sessionID + "/contexts/C_PARAM_QUIZ",
                    "lifespanCount": 99,
                    "parameters": {
                        "lstQuestionPose": lstQuestion
                    }
                },
                {
                    "name": sessionID + "/contexts/C_QUIZ",
                    "lifespanCount": 15,
                    "parameters": {}
                }
            ],
            "followupEventInput": {
                "name": "E_QUESTION{0}".format(reponse['nouvelleQuestion']),
                "languageCode": "fr-fr"
            }
        }

    def selectQuiz_message(**kwargs):
        if DEBUG:
            print("DEBUG : selectQuiz_message")
        question = kwargs['reponse']
        request = kwargs['request']
        sessionID = kwargs['session']

        laQuestion = question

        lstQuestion = []
        lstQuestion.append(question)

        if type(question) is dict:
            if 'nouvelleQuestion' in question:
                lstQuestion = request['queryResult']['outputContexts'][
                    0]['parameters']['lstQuestionPose']
                laQuestion = question['nouvelleQuestion']

        derniereQuestion = 0
        if len(lstQuestion) > 1:
            derniereQuestion = int(lstQuestion[-2])

        if laQuestion == -1:
            derniereQuestion = int(lstQuestion[-1])

        if(laQuestion == -1):
            return {
                "outputContexts": [
                    {
                        "name": sessionID + "/contexts/c_question{0}".format(derniereQuestion),
                        "lifespanCount": 0,
                        "parameters": {}
                    },
                    {
                        "name": sessionID + "/contexts/c_param_quiz",
                        "lifespanCount": 0,
                        "parameters": {}
                    }
                ],
                "followupEventInput": {
                    "name": "E_QUIZ_TERMINE",
                    "languageCode": "fr-fr"
                }
            }
        else:
            return {
                "outputContexts": [
                    {
                        "name": sessionID + "/contexts/c_question{0}".format(derniereQuestion),
                        "lifespanCount": 0,
                        "parameters": {}
                    },
                    {
                        "name": sessionID + "/contexts/C_PARAM_QUIZ",
                        "lifespanCount": 15,
                        "parameters": {
                            "lstQuestionPose": lstQuestion,
                        }
                    }
                ],
                "followupEventInput": {
                    "name": "E_QUESTION{0}".format(laQuestion),
                    "languageCode": "fr-fr"
                }
            }

    def getInformationAnnuaire_message(**kwargs):
        if DEBUG:
            print("DEBUG : getInformationAnnuaire_message start")
        response = kwargs['reponse']
        request = kwargs['request']
        sessionID = kwargs['session']

        # Aucune correspondance
        if(response is None):
            print("getInformationAnnuaire_message : Pas de correspondance")
            return {
                "source": "webhook",
                "followupEventInput": {
                    "name": "erreurFiltre",
                    "languageCode": "fr-fr"
                }
            }

        # Plusieurs prénoms pour un nom, l'utilsateur doit faire un choix
        if(type(response) is list):
            print("getInformationAnnuaire_message : Plusieurs prénoms")
            # lstPrenom = []
            # for u in response:
            #    lstPrenom.append(u.prenom)

            lstPrenom = '.. '.join([u.prenom for u in response])

            return {
                "source": "webhook-echo-sample",
                "outputContexts": [
                    {
                        "name": sessionID + "/contexts/c_ldap_temp",
                        "lifespanCount": 15,
                        "parameters": {
                            "prenoms": lstPrenom,
                            "intentOrigine": request['queryResult']['intent']['displayName'],
                            "nomTemp": response[0].nom
                        }
                    }
                ],
                "followupEventInput": {
                    "name": "E_LDAP_CHOIX_PRENOM",
                    "languageCode": "fr-fr"
                }
            }

        # Une correspondance
        if(type(response) is User):
            print("getInformationAnnuaire_message : OK. Une seule correspondance")
            if DEBUG:
                print("DEBUG : getInformationAnnuaire_message intentOrigine=", request[
                      'queryResult']['intent']['displayName'])
            return {
                "source": "webhook-echo-sample",
                "outputContexts": [
                    {
                        "name": sessionID + "/contexts/c_ldap_reponse",
                        "lifespanCount": 0
                    },
                    {
                        "name": sessionID + "/contexts/c_ldap",
                        "lifespanCount": 15,
                        "parameters": {
                            "prenom": response.prenom,
                            "nom": response.nom
                        }
                    },
                    {
                        "name": sessionID + "/contexts/c_temp",
                        "lifespanCount": 15,
                        "parameters": {
                            "nom2": response.nom,
                            "prenom2": response.prenom,
                            "telephone": util.formatTelephone(response.telephone),
                            "batiment": response.batiment,
                            "intentOrigine": request['queryResult']['intent']['displayName']
                        }
                    }
                ],
                "followupEventInput": {
                    "name": "transfert",
                    "languageCode": "fr-fr"
                }
            }

    def retourtransfert_message(**kwargs):
        response = kwargs['reponse']
        request = kwargs['request']
        sessionID = kwargs['session']
        if DEBUG:
            print("DEBUG : retourtransfert_message start")
            util.debugAllContextV2(request, sessionID)
        event = ""
        leContext = util.getContextV2(request, 'c_ldap_temp', sessionID)
        if leContext is not None:
            event = util.getCibleV2(leContext)
        else:
            leContext = util.getContextV2(request, 'c_temp', sessionID)
            event = util.getCibleV2(leContext)
        if DEBUG:
            print("DEBUG : retourtransfert_message event=", event)

        nom = response[1].get('nom2')
        prenom = response[1].get('prenom2')
        batiment = response[1].get('batiment')
        telephone = response[1].get('telephone')

        return {
            "source": "webhook-echo-sample",
            "outputContexts": [
                {
                    "name": sessionID + "/contexts/c_ldap_choix_prenom",
                    "lifespanCount": 0
                },
                {
                    "name": sessionID + "/contexts/c_ldap_temp",
                    "lifespanCount": 0
                },
                {
                    "name": sessionID + "/contexts/c_temp",
                    "lifespanCount": 0
                },
                {
                    "name": sessionID + "/contexts/c_ldap_reponse",
                    "lifespanCount": 15,
                    "parameters": {
                        "prenom": prenom,
                        "nom": nom,
                        "telephone": util.formatTelephone(telephone),
                        "batiment": batiment
                    }
                },
            ],
            "followupEventInput": {
                "name": event,
                "languageCode": "fr-fr"
            }
        }


class Message():
    """
        Classe permettant de retourner un message à DialogFlow v1
            Quiz - nouvelle question
            Quiz- vérifier réponse
            Annuaire - demande de précision
            Annuaire - réponse

    """

    def verifierReponse_message(**kwargs):
        reponse = kwargs['reponse']
        request = kwargs['request']

        lstQuestion = request['result']['contexts'][
            0]['parameters']['lstQuestionPose']

        derniereQuestion = 0

        if reponse.get('nouvelleQuestion') == -1:
            derniereQuestion = int(lstQuestion[-1])
        if len(lstQuestion) > 1:
            derniereQuestion = int(lstQuestion[-2])

        if not reponse['repondu']:
            return {
                "followupEvent": {
                    "name": "E_INFORMATION_QUESTION_{0}".format(int(lstQuestion[-1]))
                }
            }

        if (reponse['nouvelleQuestion'] == -1):
            return {
                "contextOut": [
                    {
                        "name": "c_question{0}".format(derniereQuestion),
                        "lifespan": "0",
                    },
                    {
                        "name": "c_param_quiz",
                        "lifespan": "0"
                    }
                ],
                "followupEvent": {
                    "name": "E_QUIZ_TERMINE"
                }
            }

        return {
            "contextOut": [
                {
                    "name": "c_question{0}".format(derniereQuestion),
                    "lifespan": "0",
                },
                {
                    "name": "C_PARAM_QUIZ",
                    "lifespan": "99",
                    "parameters": {
                        "lstQuestionPose": lstQuestion,
                    }
                },
                {
                    "name": "C_QUIZ",
                    "lifespan": "15",
                }
            ],
            "followupEvent": {
                "name": "E_QUESTION{0}".format(reponse['nouvelleQuestion'])
            },
        }

    def selectQuiz_message(**kwargs):

        question = kwargs['reponse']
        request = kwargs['request']

        laQuestion = question

        lstQuestion = []
        lstQuestion.append(question)

        if type(question) is dict:
            if 'nouvelleQuestion' in question:
                lstQuestion = request['result']['contexts'][
                    0]['parameters']['lstQuestionPose']
                laQuestion = question['nouvelleQuestion']

        derniereQuestion = 0
        if len(lstQuestion) > 1:
            derniereQuestion = int(lstQuestion[-2])

        if laQuestion == -1:
            derniereQuestion = int(lstQuestion[-1])

        if(laQuestion == -1):
            return {
                "contextOut": [
                    {
                        "name": "c_question{0}".format(derniereQuestion),
                        "lifespan": "0",
                    },
                    {
                        "name": "c_param_quiz",
                        "lifespan": "0"
                    }
                ],
                "followupEvent": {
                    "name": "E_QUIZ_TERMINE"
                }
            }
        else:
            return {
                "contextOut": [
                    {
                        "name": "c_question{0}".format(derniereQuestion),
                        "lifespan": "0",
                    },
                    {
                        "name": "C_PARAM_QUIZ",
                        "lifespan": "15",
                        "parameters": {
                            "lstQuestionPose": lstQuestion,
                        }
                    }
                ],
                "followupEvent": {
                    "name": "E_QUESTION{0}".format(laQuestion)
                }
            }

    def getInformationAnnuaire_message(**kwargs):

        response = kwargs['reponse']
        request = kwargs['request']

        # Aucune correspondance
        if(response is None):
            print("Pas de correspondance")
            return {
                "source": "webhook",
                "followupEvent": {
                    "name": "erreurFiltre",
                }
            }

        # Plusieurs prénoms pour un nom, l'utilsateur doit faire un choix
        if(type(response) is list):
            print("Plusieurs prénoms")
            # lstPrenom = []
            # for u in response:
            #    lstPrenom.append(u.prenom)

            lstPrenom = '.. '.join([u.prenom for u in response])

            return {
                "source": "webhook-echo-sample",
                "contextOut": [
                    {
                        "name": "c_ldap_temp",
                        "lifespan": "15",
                        "parameters": {
                            "prenoms": lstPrenom,
                            "intentOrigine": request['result']['metadata']['intentName'],
                            "nomTemp": response[0].nom
                        }
                    }
                ],
                "followupEvent": {
                    "name": "E_LDAP_CHOIX_PRENOM"
                }
            }

        # Une correspondance
        if(type(response) is User):
            print("OK. Une seule correspondance")
            return {
                "source": "webhook-echo-sample",
                "contextOut": [
                    {
                        "name": "c_ldap_reponse",
                        "lifespan": 0
                    },
                    {
                        "name": "C_LDAP",
                        "lifespan": "15",
                        "parameters": {
                            "prenom": response.prenom,
                            "nom": response.nom,
                        }
                    },
                    {
                        "name": "c_temp",
                        "parameters": {
                            "nom2": response.nom,
                            "prenom2": response.prenom,
                            "telephone": util.formatTelephone(response.telephone),
                            "batiment": response.batiment,
                            "intentOrigine": request['result']['metadata']['intentName'],
                        }
                    }
                ],
                "followupEvent": {
                    "name": "transfert"
                }
            }

    def transfert_message(**kwargs):
        response = kwargs['reponse']
        request = kwargs['request']

        event = ""
        leContext = util.getContext(request, 'c_ldap_temp')
        if leContext is not None:
            event = util.getCible(leContext)
        else:
            leContext = util.getContext(request, 'c_temp')
            event = util.getCible(leContext)

        nom = response[1].get('nom2')
        prenom = response[1].get('prenom2')
        batiment = response[1].get('batiment')
        telephone = response[1].get('telephone')

        return {
            "source": "webhook-echo-sample",
            "contextOut": [
                {
                    "name": "c_ldap_choix_prenom",
                    "lifespan": "0"
                },
                {
                    "name": "c_ldap_temp",
                    "lifespan": "0"
                },
                {
                    "name": "c_temp",
                    "lifespan": "0"
                },
                {
                    "name": "c_ldap_reponse",
                    "lifespan": "15",
                    "parameters": {
                        "prenom": prenom,
                        "nom": nom,
                        "telephone": util.formatTelephone(telephone),
                        "batiment": batiment
                    }
                },
            ],
            "followupEvent": {
                "name": event
            }
        }
