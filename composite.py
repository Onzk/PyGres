from base import *


# Fonction pour créer un type composite
def create_composite_type(
    connection,  # Objet connection
    type_name,  # Nom du type
    fields,  # Champs du type
):
    try:
        # Crée la requête SQL pour les champs
        # du type composite
        fields_sql = sql.SQL(", ").join(
            [
                sql.Identifier(field_name) + sql.SQL(" ") + sql.SQL(field_type)
                for field_name, field_type in fields.items()
            ]
        )
        # Crée la requête SQL en fonction des champs
        # et de leurs types
        create_type_query = sql.SQL("CREATE TYPE {type_name} AS ({fields})").format(
            type_name=sql.Identifier(type_name), fields=fields_sql
        )
        # Exécute la requête
        execute_query(connection, create_type_query)
    except Exception as error:
        # Affiche une l'erreur en cas de problème
        print(f"Erreur lors de la création du type composite : {error}")


# Fonction pour afficher les types composites créés
# par l'utilisateur
def show_composite_type(
    connection,  # Objet connection
):
    try:
        # Requête d'extraction des informations sur les types
        # composites créés par l'utilisateur
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
        # Retourne l'exécution de la requête
        return execute_query(connection, query)
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la récupération des types composites : {error}")


# Fonction pour supprimer un type composite
def drop_composite_type(
        connection, # Objet de connection
        type_name, # Nom du type à supprimer
        ):
    try:
        # Génère le code SQL pour supprimer le type composite
        drop_type_query = sql.SQL("DROP TYPE IF EXISTS {type_name}").format(
            type_name=sql.Identifier(type_name)
        )
        # Supprime le type composite
        execute_query(connection, drop_type_query)
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la suppression du type composite : {error}")


# Fonction pour créer une table avec un type composite
def create_table_with_composite_type(
    connection, # Objet connection
    table_name, # Nom de la tabme
    composite_type_name, # Nom du type composite
    other_fields, # Autres champs de la table
):
    try:
        # Génère le code SQL pour la création des champs de
        # la table 
        fields_sql = sql.SQL(", ").join(
            [
                sql.Identifier(field_name) + sql.SQL(" ") + sql.SQL(field_type)
                for field_name, field_type in other_fields.items()
            ]
        )
        # Génère le script SQL de création de la table
        # avec le champ composite et les autres champs
        create_table_query = sql.SQL(
            "CREATE TABLE {table_name} (id SERIAL PRIMARY KEY, "
            + composite_type_name
            + " {composite_type_name}, {fields})"
        ).format(
            table_name=sql.Identifier(table_name),
            composite_type_name=sql.Identifier(composite_type_name),
            fields=fields_sql,
        )
        # Crée la table
        execute_query(connection, create_table_query)
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la création de la table : {error}")
