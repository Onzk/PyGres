from base import *

# Fonction pour créer une vue
def create_view(connection, view_name, query):
    try:
        create_view_query = sql.SQL("CREATE VIEW {view_name} AS {query}").format(
            view_name=sql.Identifier(view_name), query=sql.SQL(query)
        )
        execute_query(connection, create_view_query)
    except Exception as error:
        print(f"Erreur lors de la création de la vue : {error}")


# Fonction pour créer une vue
def show_view(connection):
    try:
        create_view_query = f"SELECT table_schema, table_name FROM information_schema.views WHERE table_schema NOT IN ('information_schema', 'pg_catalog') ORDER BY table_schema, table_name "
        return execute_query(connection, create_view_query)
    except Exception as error:
        print(f"Erreur lors de l'affichage de la liste vue : {error}")

# Fonction pour supprimer une vue
def drop_view(connection, view_name):
    try:
        drop_view_query = sql.SQL("DROP VIEW IF EXISTS {view_name}").format(
            view_name=sql.Identifier(view_name)
        )
        execute_query(connection, drop_view_query)
    except Exception as error:
        print(f"Erreur lors de la suppression de la vue : {error}")

