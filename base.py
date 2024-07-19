import psycopg2
from psycopg2 import sql

# Fonction pour se connecter à la base de données
def connect_to_db(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port=5432,
):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,  # Remplacez par votre nom d'utilisateur PostgreSQL
            password=password,  # Remplacez par votre mot de passe PostgreSQL
            host=host,
            port=port,
        )
        print("Connexion réussie à la base de données PostgreSQL")
        return connection
    except Exception as error:
        print(f"Erreur lors de la connexion à la base de données : {error}")
        return None


# Fonction pour fermer la connexion à la base de données
def close_connection(connection):
    if connection:
        connection.close()
        print("Connexion à la base de données PostgreSQL fermée")


# Fonction pour exécuter une requête SQL
def execute_query(connection, query, params=None):
    try:
        isSelect = str(query).upper().startswith("SELECT");
        cursor = connection.cursor()
        cursor.execute(query, params)
        if isSelect : data = cursor.fetchall()
        connection.commit()
        cursor.close()
        print("Requête exécutée avec succès")
        if isSelect : return data
    except Exception as error:
        print(f"Erreur lors de l'exécution de la requête : {error}")
