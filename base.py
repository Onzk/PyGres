import psycopg2
from psycopg2 import sql

# Fonction pour se connecter à la base de données
def connect_to_db(
    dbname="postgres", # Nom de la base de données
    user="postgres", # Nom d'utilisateur
    password="postgres", # Mot de passe
    host="localhost", # Adresse IP ou nom d'Hôte
    port=5432, # Port de connextion
):
    try:
        # Crée la connection à la base de données
        connection = psycopg2.connect(
            dbname=dbname, # Nom de la base de données
            user=user,  # Nom d'utilisateur
            password=password,  # Mot de passe
            host=host, # Adresse IP ou nom d'Hôte
            port=port, # Port de connextion
        )
        # Affiche que la connexion es établie
        print("Connexion réussie à la base de données PostgreSQL")
        # Retourne l'objet connexion
        return connection
    except Exception as error:
        # Affiche l'erreur produite
        print(f"Erreur lors de la connexion à la base de données : {error}")
        # Retourne None
        return None


# Fonction pour fermer la connexion à la base de données
def close_connection(connection):
    # Verifie si l'objet connection est valide (!= None)
    if connection:
        # Ferme la connection
        connection.close()
        # Affiche que la connection a bien été fermée
        print("Connexion à la base de données PostgreSQL fermée")


# Fonction pour exécuter une requête SQL
def execute_query(
        connection, # L'objet de connection
        query,  # La requête à exécuter
        params=None # Les paramètres de la requête
        ):
    try:
        # Détermine s'il s'agit d'une récupération de données
        isSelect = str(query).upper().startswith("SELECT");
        # Crée le curseur
        cursor = connection.cursor()
        # Exécute la requête
        cursor.execute(query, params)
        # Stocke les données quand il s'agit d'une récupération
        # de données
        if isSelect : data = cursor.fetchall()
        # Enregistre les changements
        connection.commit()
        # Ferme le curseur
        cursor.close()
        # Affiche que tout s'est bien passé
        print("Requête exécutée avec succès")
        # Retourne les données, s'il s'agit d'une récupération
        if isSelect : return data
    except Exception as error:
        # En cas de problème, affiche l'erreur
        print(f"Erreur lors de l'exécution de la requête : {error}")
