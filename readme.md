# PyGres - GROUPE 4
<p align="center"><br target="_blank"><img src="./assets/logo.png"  alt="Pygres Logo"/>
<p align="center">
<a href="https://github.com/laravel/framework/actions"><img src="https://github.com/laravel/framework/workflows/tests/badge.svg" alt="Build Status"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/dt/laravel/framework" alt="Total Downloads"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/v/laravel/framework" alt="Latest Stable Version"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/l/laravel/framework" alt="License"></a>
</p>

## A Propos

PyGres est un ensemble de fonctions écrites en python permettant d'interagir avec une base de données PostgreSQL. Que ce soit les vues, les transactions, les types composites et bien d'autres, `PyGres` arbore une multitude de fonctions, vous permettant d'exploiter ces concepts, directement sur une base de données PostgreSQL.

## Contexte du Projet

- **Université** : UCAO-UUT
- **Année Scolare** : 2023-2024
- **Institut** : ISTIN - Ingénieurie, Année Préparatoire
- **Cours** : Cloud & Base de Données
- **Chargé du cours** : Dr APEKE
- **Groupe** : 4 
- **Membres** : 
    - **ASSIGNON Akofala Bénédicta**, 
    - **BISSIALO Lénica Lucie**,
    - **KOUDOSSOU Messan Dhani Justin**.

## Prérequis
- Systèmes d'exploitation supportés : 
  - Windows
  - Linux
  - Mac

- Programmes :
  - Python 3.12
  - PostgreSQL 16

- Dépendances python :
  - psycopg2==2.9.9 (`pip install psycopg2`)

## Utilisation
Le fichier point d'entrée du programme est le fichir `main.py`.
Il utilise les autres modules de l'application pour fonctionner. 
```py
from base import *
from crudtable import *
from view import *
from composite import *
from transactions import *
from replications import *
```
Ensuite, il contient des exemples d'utilisation des différentes fonctions du programme.

**_NB_ : Décommentez les lignes que vous voulez exécuter pour tester le programme.**
## Modules
Voici les modules qui composent l'application.
### base.py
Pour la gestion des fonctionnalitées globales d'interaction :
```py
import psycopg2
from psycopg2 import sql
```
- Fonction pour se connecter à la base de données
```py
def connect_to_db(
    dbname="postgres",
    user="postgres",
    password="",
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
```
- Fonction pour fermer la connexion à la base de données
```py
def close_connection(connection):
    if connection:
        connection.close()
        print("Connexion à la base de données PostgreSQL fermée")
```
- Fonction pour exécuter une requête SQL
```py
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
```

### composite.py
Pour la gestion des types composite dans la base de données :
```py
from base import *
```
- Fonction pour créer un type composite
```py
def create_composite_type(connection, type_name, fields):
    try:
        fields_sql = sql.SQL(", ").join(
            [
                sql.Identifier(field_name) + sql.SQL(" ") + sql.SQL(field_type)
                for field_name, field_type in fields.items()
            ]
        )
        create_type_query = sql.SQL("CREATE TYPE {type_name} AS ({fields})").format(
            type_name=sql.Identifier(type_name), fields=fields_sql
        )
        execute_query(connection, create_type_query)
    except Exception as error:
        print(f"Erreur lors de la création du type composite : {error}")
```
- Fonction pour afficher les types composites créés par l'utilisateur
```py
def show_composite_type(connection):
    try:
        query = """SELECT n.nspname AS schema,
            pg_catalog.format_type ( t.oid, NULL ) AS name,
            t.typname AS internal_name,
            CASE
                WHEN t.typrelid != 0
                THEN CAST ( 'tuple' AS pg_catalog.text )
                WHEN t.typlen < 0
                THEN CAST ( 'var' AS pg_catalog.text )
                ELSE CAST ( t.typlen AS pg_catalog.text )
            END AS size,
            pg_catalog.array_to_string (
                ARRAY( SELECT e.enumlabel
                        FROM pg_catalog.pg_enum e
                        WHERE e.enumtypid = t.oid
                        ORDER BY e.oid ), E'\n'
                ) AS elements,
            pg_catalog.obj_description ( t.oid, 'pg_type' ) AS description
        FROM pg_catalog.pg_type t
        LEFT JOIN pg_catalog.pg_namespace n
            ON n.oid = t.typnamespace
        WHERE ( t.typrelid = 0
                OR ( SELECT c.relkind = 'c'
                        FROM pg_catalog.pg_class c
                        WHERE c.oid = t.typrelid
                    )
            )
            AND NOT EXISTS
                ( SELECT 1
                    FROM pg_catalog.pg_type el
                    WHERE el.oid = t.typelem
                        AND el.typarray = t.oid
                )
            AND n.nspname <> 'pg_catalog'
            AND n.nspname <> 'information_schema'
            AND pg_catalog.pg_type_is_visible ( t.oid )
        ORDER BY 1, 2;"""
        return execute_query(connection, query)
    except Exception as error:
        print(f"Erreur lors de la récupération des types composites : {error}")
```
- Fonction pour supprimer un type composite
```py
def drop_composite_type(connection, type_name):
    try:
        drop_type_query = sql.SQL("DROP TYPE IF EXISTS {type_name}").format(
            type_name=sql.Identifier(type_name)
        )
        execute_query(connection, drop_type_query)
    except Exception as error:
        print(f"Erreur lors de la suppression du type composite : {error}")
```
- Fonction pour créer une table avec un type composite
```py
def create_table_with_composite_type(
    connection, table_name, composite_type_name, other_fields
):
    try:
        fields_sql = sql.SQL(", ").join(
            [
                sql.Identifier(field_name) + sql.SQL(" ") + sql.SQL(field_type)
                for field_name, field_type in other_fields.items()
            ]
        )
        create_table_query = sql.SQL(
            "CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, " + composite_type_name + " {composite_type_name}, {fields})"
        ).format(
            table_name=sql.Identifier(table_name),
            composite_type_name=sql.Identifier(composite_type_name),
            fields=fields_sql,
        )
        execute_query(connection, create_table_query)
    except Exception as error:
        print(f"Erreur lors de la création de la table : {error}")
```
### crudtable.py
Pour la gestion des CRUD sur les tables :
```py
from base import *
```
- Fonction pour créer une table
```py
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
```
- Fonction pour récupérer des données
```py
def select_data(connection, table:str, fields:list = ["*"], where:str|None = None):
    query = f"SELECT {",".join(fields)} FROM {table}"
    if where and len(where) >= 1: query += (" WHERE " + where)
    return execute_query(connection, query)
```
- Fonction pour insérer des données
```py
def insert_data(connection, table, data):
    keys = data.keys()
    values = data.values()
    query = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values})").format(
        table=sql.Identifier(table),
        fields=sql.SQL(", ").join(map(sql.Identifier, keys)),
        values=sql.SQL(", ").join(sql.Placeholder() * len(keys)),
    )
    execute_query(connection, query, list(values))
```
- Fonction pour mettre à jour des données
```py
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
```
- Fonction pour supprimer des données
```py
def delete_data(connection, table, condition):
    query = sql.SQL("DELETE FROM {table} WHERE {condition}").format(
        table=sql.Identifier(table), condition=sql.SQL(condition)
    )
    execute_query(connection, query)
```
- Fonction pour récupérer des données
```py
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
```
### replications.py
Pour la gestion des réplications dans la base de données:
```py
from base import *
```
- Fonction pour créer une publication
```py
def create_publication(connection, name:str, table:str):
    try:
        execute_query(connection, f"CREATE PUBLICATION {name} FOR TABLE {table};")
        print("Publication créée avec succés")
    except Exception as error:
        print(f"Erreur lors de la création de la publication : {error}")
```
- Fonction pour créer une souscription
```py
def create_subscription(
        connection, name:str, publication:str, 
        host:str="locahost", db:str="postgres", user:str="postgres", password:str="postgres", port=5432):
    try:
        execute_query(connection, f"""CREATE SUBSCRIPTION {name} 
                      CONNECTION 'host={host} port={port} 
                      dbname={db} user={user} password={password}' PUBLICATION {publication};""")
        print("Souscription créée avec succés")
    except Exception as error:
        print(f"Erreur lors de la création de la souscription : {error}")
```
- Fonction pour afficher les publications
```py
def show_publications(conn):
    try:
        return execute_query(conn, "SELECT pubname FROM pg_publication_tables;")
    except Exception as error:
        print(f"Erreur lors de la consultation des publications : {error}")
```
- Fonction pour afficher les souscriptions
```py
def show_subscriptions(conn):
    try:
        return execute_query(conn, "SELECT subname FROM pg_subscription;")
    except Exception as error:
        print(f"Erreur lors de la consultation des souscriptions : {error}")
```
### transactions.py
Pour effectuer des transactions dans la base de données:
```py
from base import *
```
- Fonction pour activer ou désactiver l'autocommit
```py
def set_autocommit(connection, autocommit):
    try:
        connection.autocommit = autocommit
        print(f"Autocommit {'activé' if autocommit else 'désactivé'}")
    except Exception as error:
        print(f"Erreur lors du changement d'état de l'autocommit : {error}")
```
- Fonction pour lancer un commit
```py
def commit_transaction(connection):
    try:
        connection.commit()
        print("Commit lancé avec succès")
    except Exception as error:
        print(f"Erreur lors du commit : {error}")
```
- Fonction pour lancer un rollback
```py
def rollback_transaction(connection):
    try:
        connection.rollback()
        print("Rollback lancé avec succès")
    except Exception as error:
        print(f"Erreur lors du rollback : {error}")
```
### view.py
Pour la gestion des vues dans la base de données :
```py
from base import *
```
- Fonction pour créer une vue
```py
def create_view(connection, view_name, query):
    try:
        create_view_query = sql.SQL("CREATE VIEW {view_name} AS {query}").format(
            view_name=sql.Identifier(view_name), query=sql.SQL(query)
        )
        execute_query(connection, create_view_query)
    except Exception as error:
        print(f"Erreur lors de la création de la vue : {error}")
```
- Fonction pour créer une vue
```py
def show_view(connection):
    try:
        create_view_query = f"SELECT table_schema, table_name FROM information_schema.views WHERE table_schema NOT IN ('information_schema', 'pg_catalog') ORDER BY table_schema, table_name "
        return execute_query(connection, create_view_query)
    except Exception as error:
        print(f"Erreur lors de l'affichage de la liste vue : {error}")
```
- Fonction pour supprimer une vue
```py
def drop_view(connection, view_name):
    try:
        drop_view_query = sql.SQL("DROP VIEW IF EXISTS {view_name}").format(
            view_name=sql.Identifier(view_name)
        )
        execute_query(connection, drop_view_query)
    except Exception as error:
        print(f"Erreur lors de la suppression de la vue : {error}")
```


## License
Le code source de ce projet est sous licence [MIT license](https://opensource.org/licenses/MIT).