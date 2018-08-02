# MAIF DataLab Bruno CARTIGNY
# 30.07.18

# -*- coding: utf-8 -*-

"""
    Classe qui représente une personne MAIF
"""


class User():

    def __init__(self, nom, prenom, telephone, batiment):
        """
        :param nom:
        :param prenom:
        :param telephone:
        :param batiment:
        """
        self.nom = nom
        self.prenom = prenom
        self.telephone = telephone
        self.batiment = batiment

    @property
    def nom(self):
        return self.__nom

    @nom.setter
    def nom(self, nom):
        self.__nom = nom

    @property
    def prenom(self):
        return self.__prenom

    @prenom.setter
    def prenom(self, prenom):
        self.__prenom = prenom

    @property
    def batiment(self):
        return self.__batiment

    @batiment.setter
    def batiment(self, batiment):
        self.__batiment = batiment

    @property
    def telephone(self):
        return self.__telephone

    @telephone.setter
    def telephone(self, telephone):
        self.__telephone = telephone

    def equals(self, user1):

        if type(self) is not type(user1):
            return False

        if self.__telephone != user1.telephone:
            return False

        if self.__batiment != user1.batiment:
            return False

        if self.__nom.lower() != user1.nom.lower():
            return False

        if self.__prenom.lower() != user1.prenom.lower():
            return False

        return True

    def find_by_telephone(self, user1):

        if self.__telephone == user1.telephone:
            return True
        else:
            return False

    def find_by_nom_prenom(self, user1):

        if self.__nom.lower() == user1.nom.lower() and self.__prenom.lower() == user1.prenom.lower():
            return True
        else:
            return False

    def find_by_nom(self, user1):
        if self.__nom.lower() == user1.nom.lower():
            return True
        else:
            return False
