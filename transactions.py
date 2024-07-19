from base import *

# Fonction pour activer ou désactiver l'autocommit
def set_autocommit(connection, autocommit):
    try:
        connection.autocommit = autocommit
        print(f"Autocommit {'activé' if autocommit else 'désactivé'}")
    except Exception as error:
        print(f"Erreur lors du changement d'état de l'autocommit : {error}")


# Fonction pour lancer un commit
def commit_transaction(connection):
    try:
        connection.commit()
        print("Commit lancé avec succès")
    except Exception as error:
        print(f"Erreur lors du commit : {error}")


# Fonction pour lancer un rollback
def rollback_transaction(connection):
    try:
        connection.rollback()
        print("Rollback lancé avec succès")
    except Exception as error:
        print(f"Erreur lors du rollback : {error}")

