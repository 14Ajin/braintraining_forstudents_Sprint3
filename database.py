# Ajin Sivasampoo
# Braintraining_forstudents
# 16.01.2024
# database.py

import mysql.connector
import datetime
import hashlib
from tkinter import messagebox

# Declare db_connection as a global variable
db_connection = None
current_user = None

def open_dbconnection():
    """
    Open the database connection
    """
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', user='CPNV', password='Pa$$w0rd', port='3306',
                                            database='python_game_data', buffered=True, autocommit=True)

def close_dbconnection():
    """
    Close the database connection
    """
    global db_connection
    if db_connection:
        db_connection.close()

# Add the lines in the database.py script
current_user = None

def set_current_user(user):
    global current_user
    current_user = user

def get_current_user():
    return current_user

def get_current_user_pseudo(cursor):
    """
    Get the pseudo of the current logged-in user.
    """
    # Check if a user is currently logged in
    user_id = get_current_user()
    if user_id is not None:
        # Query to get the user's pseudo
        cursor.execute("SELECT Nickname FROM Users WHERE id = %s", (user_id,))
        user_pseudo = cursor.fetchone()[0]
        return user_pseudo
    else:
        return None

# Function to create a user with password and level
def create_user_with_password_and_level(cursor, pseudo, password, user_level=1):
    """
    Create a new user with a password and a level of rights.
    """
    # Hash the password for security reasons
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    query_create_user = "INSERT INTO Users (Nickname, Password, UserLevel) VALUES (%s, %s, %s)"
    cursor.execute(query_create_user, (pseudo, password_hash, user_level))
    user_id = cursor.lastrowid
    return user_id

def register_user(cursor, pseudo, password, user_level=1):
    """
    Register a new user in the database.
    """
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    query_create_user = "INSERT INTO Users (Nickname, Password, UserLevel) VALUES (%s, %s, %s)"
    cursor.execute(query_create_user, (pseudo, password_hash, user_level))
    user_id = cursor.lastrowid
    return user_id

# Function to check user credentials during login
def login_user(cursor, pseudo, password):
    """
    Log in the user and return their information if they exist.
    """
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    query_user_exist = "SELECT id, UserLevel FROM Users WHERE Nickname = %s AND Password = %s"
    cursor.execute(query_user_exist, (pseudo, password_hash))
    result = cursor.fetchone()
    return result

# Function to check user credentials
def check_user_credentials(cursor, pseudo, password):
    """
    Check user credentials.
    """
    # Hash the password for security reasons
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    query_user_exist = "SELECT id, UserLevel FROM Users WHERE Nickname = %s AND Password = %s"
    cursor.execute(query_user_exist, (pseudo, password_hash))
    result = cursor.fetchone()
    return result

# Check if a user exists in the database
def check_user_exists(cursor, pseudo):
    query_user_exist = "SELECT id, UserLevel FROM Users WHERE Nickname = %s"
    cursor.execute(query_user_exist, (pseudo,))
    result = cursor.fetchone()
    return result

# Create a user in the database
def create_user(cursor, pseudo):
    query_create_user = "INSERT INTO Users (Nickname, Password) VALUES (%s, '')"
    cursor.execute(query_create_user, (pseudo,))
    user_id = cursor.lastrowid
    return user_id

def assign_user_level(cursor, user_pseudo):
    """
    Assign level 2 to a level 2 user.
    """
    # Check if the current user has the necessary right (level 2)
    if check_user_rights(cursor, 2):
        try:
            # Get the user ID from the pseudo
            cursor.execute("SELECT id FROM Users WHERE Nickname = %s", (user_pseudo,))
            user_id = cursor.fetchone()

            # Check if the user ID is found
            if user_id is not None:
                user_id = user_id[0]

                # Update the user's level in the database
                cursor.execute("UPDATE Users SET UserLevel = 2 WHERE id = %s", (user_id,))

                # Commit and close the cursor
                db_connection.commit()

                print(f"User {user_pseudo}'s level updated successfully.")
            else:
                print(f"User with the pseudo {user_pseudo} was not found.")
        except Exception as e:
            print(f"Error assigning level to the user: {str(e)}")
    else:
        print("You do not have the necessary rights to perform this operation.")

def promote_user(cursor, pseudo):
    """
    Promote a level 1 user to level 2.
    """
    # Check if the current user has the necessary right (level 2)
    if check_user_rights(cursor, 2):
        try:
            # Use the database connection
            cursor = db_connection.cursor()

            # Get the user ID from the pseudo
            cursor.execute("SELECT id, UserLevel FROM Users WHERE Nickname = %s", (pseudo,))
            user_data = cursor.fetchone()

            # Check if the user is found and has level 1
            if user_data is not None and user_data[1] == 1:
                user_id = user_data[0]

                # Update the user's level to 2
                cursor.execute("UPDATE Users SET UserLevel = 2 WHERE id = %s", (user_id,))

                # Commit and close the cursor
                db_connection.commit()
                cursor.close()

                print(f"User {pseudo} has been successfully promoted.")
            else:
                print(f"User with the pseudo {pseudo} was not found or is already level 2.")
        except Exception as e:
            print(f"Error promoting the user: {str(e)}")
    else:
        print("You do not have the necessary rights to perform this operation.")

def check_user_rights(cursor, required_level):
    """
    Check if the user has the necessary rights (user_level >= required_level).
    """
    # Get the current user's ID
    user_id = get_current_user()

    if user_id is not None:
        # Query to get the user's level
        cursor.execute("SELECT UserLevel FROM Users WHERE id = %s", (user_id,))
        user_level = cursor.fetchone()[0]

        # Check if the user has the necessary rights
        if user_level >= required_level:
            return True
        else:
            print("You do not have the necessary rights to perform this operation.")
            return False
    else:
        print("No user is currently logged in.")
        return False

def get_user_results(cursor, user_pseudo):
    """
    Obtenir les résultats pour un utilisateur spécifique.
    """
    # Vérifiez si l'utilisateur actuel a le droit nécessaire (niveau 1)
    if check_user_rights(cursor, 1) or user_pseudo == get_current_user_pseudo(cursor):
        # Utilisez la connexion à la base de données
        cursor = db_connection.cursor()

        # Obtenez l'ID de l'utilisateur à partir du pseudo
        cursor.execute("SELECT id FROM Users WHERE Nickname = %s", (user_pseudo,))
        user_id = cursor.fetchone()

        # Vérifiez si l'ID de l'utilisateur est trouvé
        if user_id is not None:
            user_id = user_id[0]

            # Requête pour obtenir les résultats de l'utilisateur
            cursor.execute("SELECT * FROM Results WHERE fk_users_id = %s", (user_id,))
            results = cursor.fetchall()

            # Fermez le curseur
            cursor.close()

            return results
        else:
            print(f"L'utilisateur avec le pseudo {user_pseudo} n'a pas été trouvé.")
            return None
    else:
        print("Vous n'avez pas les droits nécessaires pour effectuer cette opération.")
        return None



# Create if the exercise exists in the database.
def check_exercise_exists(cursor, exercise):
    query_exercise_exist = "SELECT id FROM Exercices WHERE Name = %s"
    cursor.execute(query_exercise_exist, (exercise,))
    result = cursor.fetchone()
    return result

# Create an exercise in the database.
def create_exercise(cursor, exercise):
    query_create_exercise = "INSERT INTO Exercices (Name) VALUES (%s)"
    cursor.execute(query_create_exercise, (exercise,))
    exercise_id = cursor.lastrowid
    return exercise_id

def save_results(cursor, timestamp, duration, nbtrials, nbsuccess, user_id, exercise_id):
    """
    Save the results in the database.
    """
    query = "INSERT INTO Results (Date_Hours, Duration, Number_of_try, Number_of_Sucess, fk_users_id, fk_exercice_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (timestamp, duration, nbtrials, nbsuccess, user_id, exercise_id)
    cursor.execute(query, values)

def delete_result(cursor, selected_values):
    """
    Delete a result from the database.

    selected_values: The selected values in the results table.
    """
    try:
        # Get the pseudo and date from the selected values
        pseudo, date_hours = selected_values[0], selected_values[1]

        # Use the pseudo to get the user ID
        cursor.execute("SELECT id FROM Users WHERE Nickname = %s", (pseudo,))
        user_id = cursor.fetchone()

        # Check if the user ID is found
        if user_id is not None:
            user_id = user_id[0]

            # Use the user ID to delete the result from the database
            cursor.execute("DELETE FROM Results WHERE fk_users_id = %s AND Date_Hours = %s", (user_id, date_hours))

            # Commit
            db_connection.commit()
        else:
            print(f"User with the pseudo {pseudo} was not found.")

    except Exception as e:
        print(f"Error deleting the result: {str(e)}")

def update_result(cursor, selected_values, duration, nbtrials, nbsuccess):
    """
    Update a result in the database.
    """
    try:
        # Convert the duration to a timedelta object
        hours, minutes, seconds = map(int, duration.split(':'))

        # Get the user ID from the Users table
        cursor.execute("SELECT id FROM Users WHERE Nickname = %s", (selected_values[0],))
        user_id = cursor.fetchone()[0]

        # Update the result in the database
        cursor.execute(
            "UPDATE Results SET Duration = %s, Number_of_try = %s, Number_of_Sucess = %s WHERE fk_users_id = %s AND Date_Hours = %s",
            (duration, nbtrials, nbsuccess, user_id, selected_values[1]))

        db_connection.commit()
    except Exception as e:
        print(f"Error updating the result: {str(e)}")

def save_new_result(cursor, pseudo, exercise, duration, nbtrials, nbsuccess):
    """
    Save a new result in the database.
    """
    try:
        # Convert the duration to a timedelta object
        hours, minutes, seconds = map(int, duration.split(':'))
        duration = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

        # Check if the exercise name is valid
        valid_exercises = ['GEO01', 'INFO02', 'INFO05']
        exercise = exercise.upper()
        if exercise not in valid_exercises:
            raise ValueError(f"Invalid exercise name. Expected one of {valid_exercises}, but got {exercise}")

        # Get the user ID from the Users table
        result = check_user_exists(cursor, pseudo)
        if result is None:
            # User does not exist, create a new user
            user_id = create_user(cursor, pseudo)
            print(f"User {pseudo} has been created.")
        else:
            # User already exists, use their ID
            user_id = result[0]

        # Check if the exercise exists in the Exercices table
        result = check_exercise_exists(cursor, exercise)

        if result is None:
            # Exercise does not exist, create a new exercise
            exercise_id = create_exercise(cursor, exercise)
            print(f"Exercise {exercise} has been created.")
        else:
            # Exercise already exists, use its ID
            exercise_id = result[0]

        # Save the new result in the database
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_results(cursor, timestamp, duration, nbtrials, nbsuccess, user_id, exercise_id)

        print("Result saved successfully.")
    except ValueError as ve:
        print(f"Error saving result: {ve}")
    except Exception as e:
        print(f"Error saving result: {str(e)}")

