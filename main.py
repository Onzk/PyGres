from base import *
from crudtable import *
from view import *
from composite import *
from transactions import *
from replications import *


# Exemple d'utilisation
# DECOMMENTEZ LES LIGNES QUE VOUS SOUHAITEZ EXECUTER.
if __name__ == "__main__":
    # Se connecter à la base de données
    conn = connect_to_db()

    # Créer la table 'employees'
    # create_table(
    #     conn,
    #     "employees",
    #     ["name varchar(50)", "age int", "department varchar(50)", "hire_date date"],
    # )

    # Insérer des données dans la table 'employees'
    # insert_data(
    #     conn,
    #     "employees",
    #     {
    #         "name": "Dupont",
    #         "age": 10,
    #         "department": "Développeur",
    #         "hire_date": "2024-07-24",
    #     },
    # )

    # Récupérer des données
    # [print(x) for x in select_data(conn, "employees")]

    # # Mettre à jour des données dans la table 'employees'
    # update_data(conn, 'employees', {'department': 'Senior Développeur'}, "name = 'Dupont' AND age = 10")

    # Récupérer des données
    # [print(x) for x in select_data(conn, "employees")]

    # Supprimer des données de la table 'employees'
    # delete_data(conn, 'employees', "name = 'Dupont' ")

    # Récupérer des données
    # [print(x) for x in select_data(conn, "employees")]

    # Créer une vue
    # create_view(conn, 'employe_vue', 'SELECT name, department, age FROM employees')

    # Lister les vues
    # [print(x) for x in show_view(conn)]

    # Supprimer une vue
    # drop_view(conn, 'employe_vue')

    # Lister les vues
    # [print(x) for x in show_view(conn)]

    # Créer un type composite
    # create_composite_type(conn, 'poste', {'nom': 'VARCHAR(100)', 'type': 'VARCHAR(100)', 'categorie': 'VARCHAR(100)'})

    # Afficher les types composite
    # [print(x) for x in show_composite_type(conn)]

    # Supprimer un type composite
    # drop_composite_type(conn, 'poste')

    # Créer un type composite
    # create_composite_type(conn, 'poste', {'nom': 'VARCHAR(100)', 'type': 'VARCHAR(100)', 'categorie': 'VARCHAR(100)'})

    # Créer une table utilisant le type composite
    # create_table_with_composite_type(conn, 'emp', 'poste', {'name': 'VARCHAR(100)', 'age': 'INT'})

    # # Récupérer des données de la table 'emp'
    # results = select_data(conn, table="emp", where='(poste).nom = \'Développeur\'')
    # for row in results:
    #     print(row)

    # Activer l'autocommit
    # set_autocommit(conn, True)

    # Désactiver l'autocommit
    # set_autocommit(conn, False)

    # Insérer des données avec des transactions
    # try:
    #         insert_data(conn, 'emp', {'poste': ('NomPoste', 'TypePoste', 'CategoriePoste'), 'name': 'Dupont', 'age': 30})
    #         # Lancer un commit
    #         commit_transaction(conn)
    # except Exception as error:
    #         print(f"Erreur lors de l'insertion : {error}")
    #         # Lancer un rollback en cas d'erreur
    #         rollback_transaction(conn)

    # Créer une publication
    # create_publication(conn, "pub_employees", "employees")

    # Afficher les publications
    # [print(x) for x in show_publications(conn)]

    # Créer une souscription
    # create_subscription(conn, "sub_employees", "pub_employees")

     # Afficher les souscriptions
    # [print(x) for x in show_subscriptions(conn)]

    # Fermer la connexion
    close_connection(conn)
