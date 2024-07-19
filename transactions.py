from base import *

# Fonction pour activer ou désactiver l'autocommit
def set_autocommit(
        connection, # Objet connection
        autocommit, # Valeur de l'Autocommit
        ):
    try:
        # Change l'autocommit sur l'objet connection
        connection.autocommit = autocommit
        # Affiche l'état de l'autocommit
        print(f"Autocommit {'activé' if autocommit else 'désactivé'}")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors du changement d'état de l'autocommit : {error}")


# Fonction pour lancer un commit
def commit_transaction(
        connection, # Objet connection
        ):
    try:
        # Lance un commit
        connection.commit()
        # Affiche que le commit a été lancé
        print("Commit lancé avec succès")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors du commit : {error}")


# Fonction pour lancer un rollback
def rollback_transaction(
        connection, # Objet connection
        ):
    try:
        # Annule les modifications
        connection.rollback()
        # Affiche que les modifications ont été annulées
        print("Rollback lancé avec succès")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors du rollback : {error}")

