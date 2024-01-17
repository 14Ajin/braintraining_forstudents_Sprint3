# Ajin Sivasampoo
# Braintraining_forstudents
# 16.01.2024
# display_result.py

import tkinter as tk
from tkinter import ttk, messagebox
import database
import datetime

# Update the display_result function signature in display_result.py
def display_result(cursor, window, user_id=None, pseudo=None):
    """
    Display the training results in a new window.
    """
    print("display_result")
    result_window = tk.Toplevel(window)
    result_window.title("Entraînement : affichage")

    # ... (le reste du code reste inchangé)


    # Définition de la couleur
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color  # traduction en hexa
    result_window.configure(bg=hex_color)

    # Créer une étiquette de titre pour la table
    table_title = tk.Label(result_window, text="Entraînement : affichage", font=("Arial", 15))
    table_title.pack()

    # Créer un cadre pour contenir les étiquettes et les saisies
    frame = tk.Frame(result_window)
    frame.pack(padx=20, pady=20)  # Ajouter un peu de marge pour l'espacement

    # Créer des étiquettes et des champs de saisie pour la saisie du pseudo et de l'exercice
    student_label = tk.Label(frame, text="Pseudo :")
    student_label.grid(row=0, column=0)
    student_entry = tk.Entry(frame)
    student_entry.grid(row=0, column=1)

    exercise_label = tk.Label(frame, text="Nom de l'exercice :")
    exercise_label.grid(row=0, column=2)
    exercise_entry = tk.Entry(frame)
    exercise_entry.grid(row=0, column=3)

    # Créer des étiquettes et des champs de saisie pour la saisie de la date
    start_date_label = tk.Label(frame, text="Date de début (YYYY-MM-DD) :")
    start_date_label.grid(row=1, column=0)
    start_date_entry = tk.Entry(frame)
    start_date_entry.grid(row=1, column=1)

    end_date_label = tk.Label(frame, text="Date de fin (YYYY-MM-DD) :")
    end_date_label.grid(row=1, column=2)
    end_date_entry = tk.Entry(frame)
    end_date_entry.grid(row=1, column=3)

    # Fonction pour mettre à jour la table des résultats
    def update_table():
        try:
            # Effacer les lignes existantes de la table
            for row in table.get_children():
                table.delete(row)

            # Ouvrir la connexion à la base de données
            database.open_dbconnection()
            cursor = database.db_connection.cursor()

            # Obtenir les valeurs du filtre depuis les saisies
            pseudo = student_entry.get()
            exercise = exercise_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()

            # Afficher les valeurs du filtre
            print(f"Pseudo : {pseudo}")
            print(f"Exercice : {exercise}")
            print(f"Date de début : {start_date}")
            print(f"Date de fin : {end_date}")

            # Vérifier si la date de fin est antérieure à la date de début
            if start_date and end_date and end_date < start_date:
                messagebox.showerror("Erreur", "La date de fin ne peut pas être antérieure à la date de début.")
                return

            # Créer la requête SQL
            query = "SELECT Users.Nickname, Results.Date_Hours, Results.Duration, Results.Number_of_try, Results.Number_of_Sucess, Exercices.Name FROM Results INNER JOIN Users ON Results.fk_users_id = Users.id INNER JOIN Exercices ON Results.fk_exercice_id = Exercices.id"
            params = []

            # Ajouter des conditions à la requête en fonction des valeurs saisies
            if pseudo:
                query += " AND Users.Nickname = %s"
                params.append(pseudo)
            if exercise:
                query += " AND Exercices.Name = %s"
                params.append(exercise)
            if start_date:
                query += " AND Results.Date_Hours >= %s"
                params.append(start_date)
            if end_date:
                query += " AND Results.Date_Hours <= %s"
                params.append(end_date)

            # Exécuter la requête
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Fermer la connexion à la base de données
            database.close_dbconnection()

            # Ajouter les données mises à jour à la table
            for row in rows:
                table.insert('', 'end', values=row)

            # Forcer la fenêtre à se rafraîchir
            result_window.update_idletasks()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la mise à jour de la table : {str(e)}")

    # Fonction pour supprimer un résultat
    def delete_result():
        try:
            # Vérifier si la table est vide
            if not table.get_children():
                messagebox.showwarning("Attention", "La table est vide. Aucun résultat à supprimer.")
                return

            # Obtenir l'élément sélectionné
            selected_item = table.selection()[0]
            # Obtenir les valeurs de l'élément sélectionné
            selected_values = table.item(selected_item, "values")
            # Supprimer le résultat de la base de données
            database.delete_result(cursor, selected_values)
            # Mettre à jour la table
            update_table()

            # Forcer l'actualisation de la fenêtre
            result_window.update_idletasks()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la suppression du résultat : {str(e)}")

    # Fonction pour mettre à jour un résultat
    def update_result():
        # Obtenir l'élément sélectionné
        selected_item = table.selection()[0]
        # Obtenir les valeurs de l'élément sélectionné
        selected_values = table.item(selected_item, "values")

        # Ouvrir une nouvelle fenêtre pour entrer les valeurs pour le résultat mis à jour
        update_window = tk.Toplevel(result_window)
        update_window.title("Mettre à jour un résultat")

        # Créer des étiquettes et des champs de saisie pour les valeurs du résultat mis à jour
        duration_label = tk.Label(update_window, text="Durée (HH:MM:SS) :")
        duration_label.pack()
        duration_entry = tk.Entry(update_window)
        duration_entry.insert(0, selected_values[2])  # Pré-remplir avec la valeur actuelle
        duration_entry.pack()

        nbtrials_label = tk.Label(update_window, text="Nombre total d'essais :")
        nbtrials_label.pack()
        nbtrials_entry = tk.Entry(update_window)
        nbtrials_entry.insert(0, selected_values[3])  # Pré-remplir avec la valeur actuelle
        nbtrials_entry.pack()

        nbsuccess_label = tk.Label(update_window, text="Nombre d'essais réussis :")
        nbsuccess_label.pack()
        nbsuccess_entry = tk.Entry(update_window)
        nbsuccess_entry.insert(0, selected_values[4])  # Pré-remplir avec la valeur actuelle
        nbsuccess_entry.pack()

        def save_updated_result():
            try:
                # Obtenir les valeurs des champs de saisie
                duration_str = duration_entry.get()
                nbtrials = int(nbtrials_entry.get())
                nbsuccess = int(nbsuccess_entry.get())

                # Convertir la durée en un objet timedelta
                hours, minutes, seconds = map(int, duration_str.split(':'))
                duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

                # Vérifier que le nombre total d'essais n'est pas inférieur au nombre d'essais réussis
                if nbtrials < nbsuccess:
                    messagebox.showerror("Erreur",
                                         "Le nombre total d'essais ne peut pas être inférieur au nombre d'essais réussis.")
                    return

                # Mettre à jour le résultat dans la base de données
                database.update_result(cursor, selected_values, duration, nbtrials, nbsuccess)

                # Fermer la fenêtre de mise à jour
                update_window.destroy()

                # Mettre à jour la table
                update_table()

                # Forcer l'actualisation de la fenêtre
                result_window.update_idletasks()
            except Exception as e:
                messagebox.showerror("Erreur",
                                     f"Une erreur s'est produite lors de la mise à jour du résultat : {str(e)}")

        # Créer un bouton pour sauvegarder le résultat mis à jour
        save_button = tk.Button(update_window, text="Sauvegarder", command=save_updated_result)
        save_button.pack()

    # Fonction pour créer un résultat
    def create_result():
        # Ouvrir une nouvelle fenêtre pour entrer les valeurs pour le nouveau résultat
        create_window = tk.Toplevel(result_window)
        create_window.title("Créer un résultat")

        # Créer des étiquettes et des champs de saisie pour les valeurs du nouveau résultat
        pseudo_label = tk.Label(create_window, text="Pseudo :")
        pseudo_label.pack()
        pseudo_entry = tk.Entry(create_window)
        pseudo_entry.pack()

        exercise_label = tk.Label(create_window, text="Nom de l'exercice :")
        exercise_label.pack()
        exercise_entry = tk.Entry(create_window)
        exercise_entry.pack()

        duration_label = tk.Label(create_window, text="Durée (HH:MM:SS) :")
        duration_label.pack()
        duration_entry = tk.Entry(create_window)
        duration_entry.pack()

        nbtrials_label = tk.Label(create_window, text="Nombre total d'essais :")
        nbtrials_label.pack()
        nbtrials_entry = tk.Entry(create_window)
        nbtrials_entry.pack()

        nbsuccess_label = tk.Label(create_window, text="Nombre d'essais réussis :")
        nbsuccess_label.pack()
        nbsuccess_entry = tk.Entry(create_window)
        nbsuccess_entry.pack()

        # Fonction pour sauvegarder un nouveau résultat
        def save_new_result():
            try:
                # Obtenir les valeurs des champs de saisie
                pseudo = pseudo_entry.get()
                exercise = exercise_entry.get().upper()  # Convertir le nom de l'exercice en majuscules
                duration = duration_entry.get()
                nbtrials = int(nbtrials_entry.get())
                nbsuccess = int(nbsuccess_entry.get())

                # Vérifier que le nombre total d'essais n'est pas inférieur au nombre d'essais réussis
                if nbtrials < nbsuccess:
                    messagebox.showerror("Erreur",
                                         "Le nombre total d'essais ne peut pas être inférieur au nombre d'essais réussis.")
                    return

                # Vérifier que le nombre total d'essais et le nombre d'essais réussis ne sont pas négatifs
                if nbtrials < 0 or nbsuccess < 0:
                    messagebox.showerror("Erreur",
                                         "Le nombre total d'essais et le nombre d'essais réussis ne peuvent pas être négatifs.")
                    return

                # Enregistrer le nouveau résultat dans la base de données
                database.save_new_result(cursor, pseudo, exercise, duration, nbtrials, nbsuccess)

                # Fermer la fenêtre de création
                create_window.destroy()

                # Mettre à jour la table
                update_table()

                # Forcer l'actualisation de la fenêtre
                result_window.update_idletasks()
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la création du résultat : {str(e)}")

        # Créer un bouton pour sauvegarder le nouveau résultat
        save_button = tk.Button(create_window, text="Sauvegarder", command=save_new_result)
        save_button.pack()

    # Create a button to update the table
    update_button = tk.Button(frame, text="Voir résultat", command=update_table)
    update_button.grid(row=2, column=1)

    # Open the database connection
    database.open_dbconnection()
    cursor = database.db_connection.cursor()

    # Fetch data from the database
    cursor.execute(
        "SELECT Users.Nickname, Results.Date_Hours, Results.Duration, Results.Number_of_try, Results.Number_of_Sucess, Exercices.Name FROM Results INNER JOIN Users ON Results.fk_users_id = Users.id INNER JOIN Exercices ON Results.fk_exercice_id = Exercices.id"
    )

    rows = cursor.fetchall()

    # Create a table to display the results
    table = ttk.Treeview(result_window)
    table['columns'] = (
        'Pseudo', 'Date Heure', 'Durée', 'Nombre total d\'essais', 'Nombre d\'essais réussis', 'Nom de l\'exercice')
    table.column('#0', width=0, stretch=tk.NO)
    table.column('Pseudo', anchor=tk.CENTER, width=80)
    table.column('Date Heure', anchor=tk.CENTER, width=80)
    table.column('Durée', anchor=tk.CENTER, width=80)
    table.column('Nombre total d\'essais', anchor=tk.CENTER, width=80)
    table.column('Nombre d\'essais réussis', anchor=tk.CENTER, width=80)
    table.column('Nom de l\'exercice', anchor=tk.CENTER, width=80)

    table.heading('#0', text='', anchor=tk.CENTER)
    table.heading('Pseudo', text='Pseudo', anchor=tk.CENTER)
    table.heading('Date Heure', text='Date Heure', anchor=tk.CENTER)
    table.heading('Durée', text='Durée', anchor=tk.CENTER)
    table.heading('Nombre total d\'essais', text='Nombre total d\'essais', anchor=tk.CENTER)
    table.heading('Nombre d\'essais réussis', text='Nombre d\'essais réussis', anchor=tk.CENTER)
    table.heading('Nom de l\'exercice', text='Nom de l\'exercice', anchor=tk.CENTER)

    # Insert the rows into the table
    for row in rows:
        table.insert('', 'end', values=row)

    table.pack()

    # Create buttons for each action
    delete_button = tk.Button(result_window, text="Supprimer le résultat", command=delete_result)
    delete_button.pack()

    update_button = tk.Button(result_window, text="Mettre à jour le résultat", command=update_result)
    update_button.pack()

    create_button = tk.Button(result_window, text="Créer un résultat", command=create_result)
    create_button.pack()

