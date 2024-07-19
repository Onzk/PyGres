from base import *


# Fonction pour créer une publication
def create_publication(connection, name:str, table:str):
    try:
        execute_query(connection, f"CREATE PUBLICATION {name} FOR TABLE {table};")
        print("Publication créée avec succés")
    except Exception as error:
        print(f"Erreur lors de la création de la publication : {error}")


# Fonction pour créer une souscription
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

# Fonction pour afficher les publications
def show_publications(conn):
    try:
        return execute_query(conn, "SELECT pubname FROM pg_publication_tables;")
    except Exception as error:
        print(f"Erreur lors de la consultation des publications : {error}")

# Fonction pour afficher les souscriptions
def show_subscriptions(conn):
    try:
        return execute_query(conn, "SELECT subname FROM pg_subscription;")
    except Exception as error:
        print(f"Erreur lors de la consultation des souscriptions : {error}")
