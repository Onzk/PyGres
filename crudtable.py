from base import *


# Fonction pour créer une table
def create_table(connection, table, fields: list, autoId=True):
    try:
        if autoId:
            fields = ["id SERIAL PRIMARY KEY"] + fields
        execute_query(
            connection,
            f"CREATE TABLE IF NOT EXISTS {table} (" + ",".join(fields)+ ");",
        )
        print(f"Table {table}, créée avec succès.")
    except Exception as error:
        print("Impossible de créer la table. Erreur : " + repr(error))


# Fonction pour récupérer des données
def select_data(connection, table:str, fields:list = ["*"], where:str|None = None):
    query = f"SELECT {",".join(fields)} FROM {table}"
    if where and len(where) >= 1: query += (" WHERE " + where)
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
def update_data(connection, table, data, condition):
    keys = data.keys()
    values = list(data.values())
    query = sql.SQL("UPDATE {table} SET {fields} WHERE {condition}").format(
        table=sql.Identifier(table),
        fields=sql.SQL(", ").join(
            sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder()])
            for k in keys
        ),
        condition=sql.SQL(condition),
    )
    execute_query(connection, query, values)


# Fonction pour supprimer des données
def delete_data(connection, table, condition):
    query = sql.SQL("DELETE FROM {table} WHERE {condition}").format(
        table=sql.Identifier(table), condition=sql.SQL(condition)
    )
    execute_query(connection, query)


# Fonction pour récupérer des données
def fetch_data(connection, query, params=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
    except Exception as error:
        print(f"Erreur lors de la récupération des données : {error}")
        return None

