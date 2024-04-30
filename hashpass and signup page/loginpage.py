import psycopg2
import hashlib

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="673636",
            host="localhost",
            port="5432"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

# Function to register a new user
def register_user(username, name, password):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Check if the username already exists
        select_user_query = """SELECT username FROM "user" WHERE username = %s"""
        cursor.execute(select_user_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            print("Username already exists. Please choose a different username.")
            return

        # Hash the password
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Store the hashed password and other details in the "user" table
        insert_user_query = """INSERT INTO "user" (username, name, hashed_password) VALUES (%s, %s, %s)"""
        cursor.execute(insert_user_query, (username, name, hashed_password))

        connection.commit()
        print("User registered successfully!")
    except (Exception, psycopg2.Error) as error:
        print("Error registering user:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Function to authenticate a user
def authenticate_user(username, password):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        # Retrieve the hashed password from the "user" table
        select_query = """SELECT hashed_password FROM "user" WHERE username = %s"""
        cursor.execute(select_query, (username,))
        user_data = cursor.fetchone()

        if user_data:
            hashed_password = user_data[0]
        
            # Hash the provided password
            provided_password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Compare the hashed password with the one stored in the database
            if provided_password_hash == hashed_password:
                print("Authentication successful!")
            else:
                print("Incorrect password. Authentication failed.")
        else:
            print("User not found.")
    except (Exception, psycopg2.Error) as error:
        print("Error authenticating user:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


# Example usage
#####################TESTTTTTTTTT######################
#register_user("my_username", "John Doe", "my_secure_password")
#authenticate_user("my_username", "my_secure_password")
# Known passwords for the users
known_passwords = {
    "user_0": "password123",
    "user_1": "qwerty456",
    "user_2": "abc123def",
    "user_3": "letmein789",
    "user_4": "securepass"
}

# Register users
for i in range(5):
    username = f"user_{i}"
    name = f"User {i}"
    password = known_passwords.get(username)
    register_user(username, name, password)

# Authenticate users
if register_user:
    for i in range(5):
        username = f"user_{i}"
        password = input(f"Enter password for {username}: ")
        authenticate_user(username, password)


