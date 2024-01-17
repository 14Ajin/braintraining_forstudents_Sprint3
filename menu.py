# Ajin Sivasampoo
# Braintraining_forstudents
# 16.01.2024
# menu.py

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
import hashlib
import geo01
import info02
import info05
import database
from display_result import display_result
from database import promote_user

# Declare main_window
main_window = None
user_level = 0  # Variable pour stocker le niveau de l'utilisateur connecté
user_id = None  # Variable pour stocker l'ID de l'utilisateur connecté

# Global variables
global update_table_button_pressed
update_table_button_pressed = False
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None]  # tableau d'étiquettes (avec images)
a_image = [None, None, None]  # tableau d'images
a_title = [None, None, None]  # tableau de titres (ex: GEO01)

# Modify this call to take main_window into account
dict_games = {
    "geo01": lambda: geo01.open_window_geo_01(main_window),
    "info02": lambda: info02.open_window_info_02(main_window),
    "info05": lambda: info05.open_window_info_05(main_window)
}

# Appeler d'autres fenêtres (exercices)
def exercise(exer):
    try:
        if user_level == 1 and exer in a_exercise:
            messagebox.showinfo("Info", "You can only see your own results.")
        else:
            dict_games[exer]()  # Use main_window directly, as it is now a global variable
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")


# Variable Pseudo
pseudo = ""
user_level_var = None

# Function to create the variable user_level_var after the creation of the main window
def create_user_level_var():
    global user_level_var, main_window
    user_level_var = tk.IntVar()
    main_window = tk.Tk()
    main_window.withdraw()  # Hide the main window initially


# Function to open the registration window
def open_window_register():
    global pseudo, user_level_var
    register_window = tk.Toplevel(main_window)
    register_window.title("Register")

    tk.Label(register_window, text="Pseudo").grid(row=0)
    pseudo_entry = tk.Entry(register_window)
    pseudo_entry.grid(row=0, column=1)

    tk.Label(register_window, text="Mot de passe").grid(row=1)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(register_window, text="Confirmer le mot de passe").grid(row=2)
    confirm_password_entry = tk.Entry(register_window, show="*")
    confirm_password_entry.grid(row=2, column=1)

    tk.Label(register_window, text="Niveau").grid(row=3)
    level_var = tk.IntVar()
    level_checkbox_1 = tk.Checkbutton(register_window, text="Niveau 1", variable=level_var, onvalue=1)
    level_checkbox_1.grid(row=3, column=1)

    level_checkbox_2 = tk.Checkbutton(register_window, text="Niveau 2", variable=level_var, onvalue=2)
    level_checkbox_2.grid(row=3, column=2)

    def submit():
        try:
            global pseudo, user_level

            new_pseudo = pseudo_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            level = level_var.get()

            if password != confirm_password:
                messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
                return

            password_hash = hashlib.sha256(password.encode()).hexdigest()

            database.open_dbconnection()
            cursor = database.db_connection.cursor()

            if database.check_user_exists(cursor, new_pseudo):
                messagebox.showerror("Erreur", "Ce pseudo est déjà pris.")
                return

            user_id = database.create_user_with_password_and_level(cursor, new_pseudo, password_hash, level)

            if user_id is not None:
                messagebox.showinfo("Succès", "Inscription réussie. Vous pouvez maintenant vous connecter.")
                register_window.destroy()
            else:
                messagebox.showerror("Erreur", "L'inscription a échoué.")

        except database.DatabaseError as db_error:
            messagebox.showerror("Erreur de base de données", f"Erreur de base de données : {str(db_error)}")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

        finally:
            database.close_dbconnection()

    submit_button = tk.Button(register_window, text="Submit", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Function to log in
def login():
    try:
        global pseudo, user_level, user_id

        database.open_dbconnection()
        cursor = database.db_connection.cursor()

        pseudo = pseudo_entry.get()
        password = password_entry.get()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        user_data = database.check_user_credentials(cursor, pseudo, password_hash)

        if user_data is not None:
            user_id, user_level = user_data
            login_window.destroy()
            open_menu_window(cursor)
        else:
            messagebox.showerror("Erreur", "Pseudo ou mot de passe incorrect.")

    except database.DatabaseError as db_error:
        messagebox.showerror("Erreur de base de données", f"Erreur de base de données : {str(db_error)}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    finally:
        database.close_dbconnection()

# Function to log out
def logout():
    global main_window, pseudo, login_window, user_level, user_id
    if main_window:
        main_window.destroy()
    pseudo = ""
    user_level = 0
    user_id = None
    login_window.deiconify()

# Function to open the menu window
def open_menu_window(cursor):
    try:
        global main_window, user_level, user_id, pseudo

        main_window = tk.Tk()
        main_window.title("Entraînement, entraînement cérébral")
        main_window.geometry("1100x900")

        rgb_color = (139, 201, 194)
        hex_color = '#%02x%02x%02x' % rgb_color
        main_window.configure(bg=hex_color)
        main_window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

        lbl_title = tk.Label(main_window, text="MENU D'ENTRAÎNEMENT", font=("Arial", 15))
        lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

        for ex in range(len(a_exercise)):
            a_title[ex] = tk.Label(main_window, text=a_exercise[ex], font=("Arial", 15))
            a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)

            a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")
            albl_image[ex] = tk.Label(main_window, image=a_image[ex])
            albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)

            a_title[ex].bind("<Button-1>", lambda e, exer=a_exercise[ex]: exercise(exer))
            albl_image[ex].bind("<Button-1>", lambda e, exer=a_exercise[ex]: exercise(exer))

        btn_ranking = tk.Button(main_window, text="Afficher le classement", font=("Arial", 15),
                                command=lambda: display_result_window(cursor))

        btn_ranking.grid(row=3 + 2 * len(a_exercise) // 3, column=0, columnspan=3, pady=10)

        btn_disconnect = tk.Button(main_window, text="Déconnexion", font=("Arial", 15), command=logout)
        btn_disconnect.grid(row=4 + 2 * len(a_exercise) // 3, column=0, columnspan=3, pady=10)

        btn_quit = tk.Button(main_window, text="Quitter", font=("Arial", 15), command=main_window.destroy)
        btn_quit.grid(row=5 + 2 * len(a_exercise) // 3, column=0, columnspan=3, pady=10)

        if user_level == 2:
            # Ajout du bouton pour promouvoir un utilisateur au niveau 2
            btn_promote_user = tk.Button(main_window, text="Promouvoir Utilisateur", font=("Arial", 15),
                                         command=lambda: promote_user(cursor, pseudo))
            btn_promote_user.grid(row=6 + 2 * len(a_exercise) // 3, column=0, columnspan=3, pady=10)

            # Ajout de l'étiquette pour afficher le pseudo
        pseudo_label = tk.Label(main_window, text=f"Bienvenue, {pseudo}!", font=("Arial", 12), fg="black")
        pseudo_label.grid(row=4 + 2 * len(a_exercise) // 3, column=0, columnspan=3, pady=10)

        # Ajout de l'étiquette pour afficher le niveau de l'utilisateur
        level_label = tk.Label(main_window, text=f"Niveau de l'utilisateur : {user_level}", font=("Arial", 12),
                               fg="black")
        level_label.grid(row=5 + 2 * len(a_exercise) // 3, column=0, columnspan=3, pady=10)

        main_window.protocol("WM_DELETE_WINDOW", on_closing)
        main_window.mainloop()

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

# Function to confirm window closing
def on_closing():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        main_window.destroy()

# Function to open the ranking windown
def display_result_window(cursor):
    global main_window, user_id, user_level, pseudo

    try:
        database.open_dbconnection()
        cursor = database.db_connection.cursor()

        if user_level == 2:
            # Les utilisateurs de niveau 2 peuvent voir les résultats de tous les utilisateurs
            display_result(cursor, main_window)
        else:
            # Les utilisateurs de niveau 1 peuvent voir leurs propres résultats uniquement
            display_result(cursor, main_window, user_id, pseudo)

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    finally:
        database.close_dbconnection()


# Function to open the login window
def open_login_window():
    global pseudo_entry, password_entry, login_window, user_level_var

    login_window = tk.Tk()
    login_window.title("Login")

    create_user_level_var()

    tk.Label(login_window, text="Pseudo").grid(row=0)
    pseudo_entry = tk.Entry(login_window)
    pseudo_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Mot de passe").grid(row=1)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    btn_login = tk.Button(login_window, text="Login", command=login)
    btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    btn_register = tk.Button(login_window, text="S'inscrire", command=open_window_register)
    btn_register.grid(row=3, column=0, columnspan=2, pady=10)

    login_window.protocol("WM_DELETE_WINDOW", on_closing)
    login_window.mainloop()


# Main program
if __name__ == "__main__":
    open_login_window()
