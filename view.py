from base import *

# Fonction pour créer une vue
def create_view(
        connection, # Objet connection
        view_name, # Nom de la vue
        query, # Requête à exécuter dans la vue
        ):
    try:
        # Génère le script SQL pour créer la vue
        create_view_query = sql.SQL("CREATE VIEW {view_name} AS {query}").format(
            view_name=sql.Identifier(view_name), query=sql.SQL(query)
        )
        # Crée la vue
        execute_query(connection, create_view_query)
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la création de la vue : {error}")


# Fonction pour créer une vue
def show_view(
        connection, # Objet connection
        ):
    try:
        # Script récupération des vues de la base de données
        create_view_query = f"SELECT table_schema, table_name FROM information_schema.views WHERE table_schema NOT IN ('information_schema', 'pg_catalog') ORDER BY table_schema, table_name "
        # Retourne la liste des vues de la base de données
        return execute_query(connection, create_view_query)
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de l'affichage de la liste vue : {error}")

# Fonction pour supprimer une vue
def drop_view(
        connection, # Objet connection
        view_name, # Nom de la vue à supprimer
        ):
    try:
        # Génère le script de suppression de la vue
        drop_view_query = sql.SQL("DROP VIEW IF EXISTS {view_name}").format(
            view_name=sql.Identifier(view_name)
        )
        # Supprime la vue
        execute_query(connection, drop_view_query)
    except Exception as error:
        # Affiche une erreur s'il y en a
        print(f"Erreur lors de la suppression de la vue : {error}")

