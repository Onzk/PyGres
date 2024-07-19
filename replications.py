from base import *


# Fonction pour créer une publication
def create_publication(
        connection, # Objet connection
        name:str, # Nom de la publication
        table:str, # Table concernée
        ):
    try:
        # Crée la publication sur la table concernée
        execute_query(connection, f"CREATE PUBLICATION {name} FOR TABLE {table};")
        # Affiche que la publication a été créée
        print("Publication créée avec succés")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la création de la publication : {error}")


# Fonction pour créer une souscription
def create_subscription(
        connection, # Objet connection
        name:str, # Nom de la souscription
        publication:str, # Nom de la publication sur laquelle souscrire
        host:str="locahost", # Adresse ou nom de l'hôte maître
        db:str="postgres", # Base de données de l'hôte maître
        user:str="postgres", # Nom d'utilisateur de l'hôte maître
        password:str="postgres", # Mot de passe du nom d'utilisateur de l'hôte maître
        port=5432, # Port de l'hôte maître
        ):
    try:
        # Création de la souscription
        execute_query(connection, f"""CREATE SUBSCRIPTION {name} 
                      CONNECTION 'host={host} port={port} 
                      dbname={db} user={user} password={password}' PUBLICATION {publication};""")
        # Affiche que la souscription a été créée
        print("Souscription créée avec succés")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la création de la souscription : {error}")

# Fonction pour afficher les publications
def show_publications(
        conn, # Objet connection
        ):
    try:
        # Retourne la liste des publications
        return execute_query(conn, "SELECT pubname FROM pg_publication_tables;")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la consultation des publications : {error}")

# Fonction pour afficher les souscriptions
def show_subscriptions(
        conn, # Objet connection
        ):
    try:
        # Retourne la liste des souscriptions
        return execute_query(conn, "SELECT subname FROM pg_subscription;")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la consultation des souscriptions : {error}")
