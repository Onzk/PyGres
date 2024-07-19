from base import *


# Fonction pour créer un type composite
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

# Fonction pour afficher les types composites créés 
# par l'utilisateur
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

# Fonction pour supprimer un type composite
def drop_composite_type(connection, type_name):
    try:
        drop_type_query = sql.SQL("DROP TYPE IF EXISTS {type_name}").format(
            type_name=sql.Identifier(type_name)
        )
        execute_query(connection, drop_type_query)
    except Exception as error:
        print(f"Erreur lors de la suppression du type composite : {error}")


# Fonction pour créer une table avec un type composite
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
