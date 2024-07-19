from base import *


# Fonction pour créer une table
def create_table(
        connection, # Objet connection
        table, # La table à créer
        fields: list, # Les champs de la table
        autoId=True, # Option pour ajouter un champs ID automatiquement
        ):
    try:
        # Si on ajoute le champ ID automatiquement
        if autoId:
            # Ajoute ID dans la liste des champs
            fields = ["id SERIAL PRIMARY KEY"] + fields
        # Crée la table avec son nom et ses champs
        execute_query(
            connection,
            f"CREATE TABLE IF NOT EXISTS {table} (" + ",".join(fields)+ ");",
        )
        # Affiche que la table a bien été créée
        print(f"Table {table}, créée avec succès.")
    except Exception as error:
        # Affiche une erreur s'il y en a
        print("Impossible de créer la table. Erreur : " + repr(error))


# Fonction pour récupérer des données
def select_data(
        connection, # Objet connection
        table:str, # Nom de la table
        fields:list = ["*"], # Les champs à sélectionner
        where:str|None = None, # Filtre sur les données
        ):
    # Requête de récupération de données
    query = f"SELECT {",".join(fields)} FROM {table}"
    # Ajoute le filtre s'il y en a
    if where and len(where) >= 1: query += (" WHERE " + where)
    # Retourne le résultat de la récupération
    return execute_query(connection, query)

# Fonction pour insérer des données
def insert_data(connection, table, data):
    keys = data.keys()
    values = data.values()
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values})").format(
        table=sql.Identifier(table),
        fields=sql.SQL(", ").join(map(sql.Identifier, keys)),
        values=sql.SQL(", ").join(sql.Placeholder() * len(keys)),
    )
    execute_query(connection, query, list(values))


# Fonction pour mettre à jour des données
def update_data(
        connection, # Objet connection
        table, # Table cible
        data, # Données mises à jour
        condition, # Filtre sur les données concernées par les modifications
        ):
    # Récupère les champs
    keys = data.keys()
    # Récupère les nouvelles valeurs
    values = list(data.values())
    # Génère le script de modification
    query = sql.SQL("UPDATE {table} SET {fields} WHERE {condition}").format(
        table=sql.Identifier(table),
        fields=sql.SQL(", ").join(
            sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder()])
            for k in keys
        ),
        condition=sql.SQL(condition),
    )
    # Exécute la modification
    execute_query(connection, query, values)


# Fonction pour supprimer des données
def delete_data(
        connection, # Objet de connection
        table, # Table en question
        condition, # Filtre sur les données concernées
        ):
    # Génère le script de suppression
    query = sql.SQL("DELETE FROM {table} WHERE {condition}").format(
        table=sql.Identifier(table), condition=sql.SQL(condition)
    )
    # Supprime les données
    execute_query(connection, query)


# Fonction pour récupérer des données
def fetch_data(
        connection, # Objet connection
        query, # Requête à exécuter
        params=None, # Paramètres de la requête
        ):
    try:
        # Crée du curseur
        cursor = connection.cursor()
        # Exécute de la requête
        cursor.execute(query, params)
        # Récupère des résultats
        results = cursor.fetchall()
        # Ferme du curseur
        cursor.close()
        # Retourne les données
        return results
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la récupération des données : {error}")
        # Retourne None
        return None

