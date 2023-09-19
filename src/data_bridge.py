import mysql.connector



def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='admin',
        password='test123',
        database='test'
    )
    return connection


def create_users_table():
    connection = get_connection()
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL      
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()


def create_entry_table():
    connection = get_connection()
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Text_Entry (
        entry_id int NOT NULL AUTO_INCREMENT,
        entry_text MEDIUMTEXT,
        user_id int,
        PRIMARY KEY (entry_id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def create_thread_table():
    connection = get_connection()
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Thread (
        thread_id int NOT NULL AUTO_INCREMENT,
        thread_name MEDIUMTEXT,
        user_id int,
        PRIMARY KEY (thread_id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()


def create_thread(thread_name, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    

    insert_query = "INSERT INTO Thread (thread_name, user_id) VALUES (%s, %s)"
    user_data = (thread_name,user_id)
    
    try:
        cursor.execute(insert_query, user_data)
        connection.commit()
        print("Thread created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def create_user(username, email, password):
    connection = get_connection()
    cursor = connection.cursor()
    

    insert_query = "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)"
    user_data = (username, email, password)
    
    try:
        cursor.execute(insert_query, user_data)
        connection.commit()
        print("User created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def create_entry(entry_text, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Use a parameterized query to insert the new entry
    insert_query = "INSERT INTO Text_Entry (entry_text, user_id) VALUES (%s, %s)"
    entry_data = (entry_text, user_id)
    
    try:
        cursor.execute(insert_query, entry_data)
        connection.commit()
        print("Entry created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def get_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Abfrage, um Benutzerdaten anhand der Benutzer-ID abzurufen
    query = "SELECT username, email FROM Users WHERE user_id = %s"
    
    try:
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()  # Holt das erste Ergebnis (es sollte nur eines geben)
        return user_data
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        cursor.close()
        connection.close()
        

def get_user_by_name(user_name):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Abfrage, um Benutzerdaten anhand der Benutzer-ID abzurufen
    query = "SELECT * FROM Users WHERE username = %s"
    
    try:
        cursor.execute(query, (user_name,))
        user_data = cursor.fetchone()  # Holt das erste Ergebnis (es sollte nur eines geben)
        return user_data
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        cursor.close()
        connection.close()

def get_entry(entry_id):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Abfrage, um Eintragsdaten anhand der Eintrags-ID abzurufen
    query = "SELECT entry_text, user_id FROM Text_Entry WHERE entry_id = %s"
    
    try:
        cursor.execute(query, (entry_id,))
        entry_data = cursor.fetchone()  # Holt das erste Ergebnis (es sollte nur eines geben)
        return entry_data
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        cursor.close()
        connection.close()

def check_credentials(user, password):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Abfrage, um Eintragsdaten anhand der Eintrags-ID abzurufen
    query = "SELECT * FROM users Text_Entry WHERE username = %s and password = %s"
    
    try:
        cursor.execute(query, (user, password))
        entry_data = cursor.fetchone()  # Holt das erste Ergebnis (es sollte nur eines geben)
        return entry_data
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        cursor.close()
        connection.close()
        
def get_threads():
    connection = get_connection()
    cursor = connection.cursor()
    
    # Abfrage, um Eintragsdaten anhand der Eintrags-ID abzurufen
    query = "SELECT * FROM Thread"
    
    try:
        cursor.execute(query)
        entry_data = cursor.fetchall()  # Holt das erste Ergebnis (es sollte nur eines geben)
        return entry_data
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    create_users_table()
    create_entry_table()
    create_thread_table()